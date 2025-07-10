package handler

import (
	"ats-scorer/service"
	"fmt"
	"github.com/gofiber/fiber/v2"
	"os"
)

func ScoreResume(c *fiber.Ctx) error {
	fileHeader, err := c.FormFile("resume")
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Resume file is required",
		})
	}

	// Save file
	filePath, err := service.SaveFile(fileHeader)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "File save failed"})
	}
	defer func(name string) {
		err := os.Remove(name)
		if err != nil {

		}
	}(filePath) // cleanup

	// get score
	score, err := service.GetScore(filePath)
	if err != nil {
		fmt.Println(err)
	}
	return c.JSON(fiber.Map{
		"filename": fileHeader.Filename,
		"score":    score,
	})
}
