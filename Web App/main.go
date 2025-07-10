package main

import (
	"log"

	"ats-scorer/handler"
	"github.com/gofiber/fiber/v2"
)

func main() {
	app := fiber.New()

	app.Post("/score", handler.ScoreResume)

	log.Fatal(app.Listen(":3000"))
}
