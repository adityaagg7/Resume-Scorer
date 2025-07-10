package service

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"os"
)

func SaveFile(fileHeader *multipart.FileHeader) (string, error) {
	tempDir := "./temp"
	if err := os.MkdirAll(tempDir, os.ModePerm); err != nil {
		return "", err
	}
	filePath := fmt.Sprintf("%s/%s", tempDir, fileHeader.Filename)
	if err := saveMultipartFile(fileHeader, filePath); err != nil {
		return "", err
	}
	return filePath, nil
}

func saveMultipartFile(fileHeader *multipart.FileHeader, filePath string) error {
	src, err := fileHeader.Open()
	if err != nil {
		return err
	}
	defer src.Close()

	dst, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer dst.Close()

	_, err = io.Copy(dst, src)
	return err
}

func GetScore(filePath string) (json.RawMessage, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)
	part, err := writer.CreateFormFile("file", file.Name())
	if err != nil {
		return nil, err
	}

	if _, err := io.Copy(part, file); err != nil {
		return nil, err
	}
	writer.Close()

	resp, err := http.Post("http://localhost:8000/score/", writer.FormDataContentType(), body)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	respData, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	fmt.Println("Response from Python scorer:", string(respData))
	return respData, nil
}
