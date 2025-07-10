package main

import (
	"github.com/gofiber/fiber/v2/middleware/cors"
	"log"

	"ats-scorer/handler"
	"github.com/gofiber/fiber/v2"
)

func main() {
	app := fiber.New()
	app.Use(cors.New(cors.Config{
		AllowOrigins: "*",
		AllowMethods: "GET,POST,OPTIONS",
		AllowHeaders: "Content-Type",
	}))
	app.Post("/score", handler.ScoreResume)

	log.Fatal(app.Listen("0.0.0.0:3000"))
}
