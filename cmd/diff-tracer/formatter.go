package main

import (
	"fmt"
)

func getPrevChar(idx int, data string) string {
	if idx == 0 {
		return ""
	}
	return fmt.Sprintf("%c", data[idx-1])
}

func getNextChar(idx int, size int, data string) string {
	if idx == size-1 {
		return ""
	}
	return fmt.Sprintf("%c", data[idx+1])
}

func formatter(data string) []string {
	currLine := ""
	result := []string{}
	currIndentation := 0

	for idx, c := range data {
		char := fmt.Sprintf("%c", c)

		if char == "{" {
			nextChar := getNextChar(idx, len(data), data)
			if nextChar == "}" {
				currLine += char
				continue
			}
			currLine += char
			result = append(result, currLine)
			currLine = ""
			currIndentation += 2
			for range currIndentation {
				currLine += " "
			}
			continue
		}

		if char == "}" {
			prevChar := getPrevChar(idx, data)
			if prevChar == "{" {
				currLine += char
				continue
			}
			currIndentation -= 2
			result = append(result, currLine)
			currLine = ""
			for range currIndentation {
				currLine += " "
			}
			currLine += char
			continue
		}

		if char == "[" {
			nextChar := getNextChar(idx, len(data), data)
			if nextChar == "]" {
				currLine += char
				continue
			}
			currLine += char
			result = append(result, currLine)
			currLine = ""
			currIndentation += 2
			for range currIndentation {
				currLine += " "
			}
			continue
		}

		if char == "]" {
			prevChar := getPrevChar(idx, data)
			if prevChar == "[" {
				currLine += char
				continue
			}
			nextChar := getNextChar(idx, len(data), data)
			currIndentation -= 2
			if nextChar == "," {
				result = append(result, currLine)
				currLine = ""
				for range currIndentation {
					currLine += " "
				}
				currLine += char
			} else {
				currLine += char
				result = append(result, currLine)
				currLine = ""
			}
			continue
		}

		if char == "," {
			currLine += char
			result = append(result, currLine)
			currLine = ""
			for range currIndentation {
				currLine += " "
			}
			continue
		}

		if char == ":" {
			prevChar := getPrevChar(idx, data)
			if prevChar == "\"" {
				currLine += char + " "
				continue
			}
		}

		currLine += char
	}

	return result
}
