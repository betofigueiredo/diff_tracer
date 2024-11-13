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

func formatter(data string) string {
	result := ""
	currIndentation := 0

	for idx, c := range data {
		char := fmt.Sprintf("%c", c)

		if char == "{" {
			nextChar := getNextChar(idx, len(data), data)
			if nextChar == "}" {
				result += char
				continue
			}
			result += char + "\n"
			currIndentation += 2
			for range currIndentation {
				result += " "
			}
			continue
		}

		if char == "}" {
			prevChar := getPrevChar(idx, data)
			if prevChar == "{" {
				result += char
				continue
			}
			currIndentation -= 2
			result += "\n"
			for range currIndentation {
				result += " "
			}
			result += char
			continue
		}

		if char == "[" {
			nextChar := getNextChar(idx, len(data), data)
			if nextChar == "]" {
				result += char
				continue
			}
			result += char + "\n"
			currIndentation += 2
			for range currIndentation {
				result += " "
			}
			continue
		}

		if char == "]" {
			prevChar := getPrevChar(idx, data)
			if prevChar == "[" {
				result += char
				continue
			}
			nextChar := getNextChar(idx, len(data), data)
			currIndentation -= 2
			if nextChar == "," {
				result += "\n"
				for range currIndentation {
					result += " "
				}
				result += char
			} else {
				result += char + "\n"
			}
			continue
		}

		if char == "," {
			result += char + "\n"
			for range currIndentation {
				result += " "
			}
			continue
		}

		if char == ":" {
			prevChar := getPrevChar(idx, data)
			if prevChar == "\"" {
				result += char + " "
				continue
			}
		}

		result += char
	}

	return result
}
