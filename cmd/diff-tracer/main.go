package main

import (
	"fmt"
	"io"
	"net/http"
)

func main() {
	resp, err := http.Get("https://anapioficeandfire.com/api/characters/581")
	if err != nil {
		fmt.Println(" [ERROR]")
	}
	defer resp.Body.Close()

	bytedata, _ := io.ReadAll(resp.Body)
	reqBodyString := string(bytedata)
	fmt.Println(reqBodyString)

	fmt.Println(" ")

	for1 := formatter(reqBodyString)
	fmt.Println(for1)

	fmt.Println(" ")

	data := `{"data":[],"meta":{"numberOfUnreadNotifications":0,"total":0,"anotherArr":[1,2],"exists":false},hash:{}}`
	formattedJSON := formatter(data)

	fmt.Println(formattedJSON)
}
