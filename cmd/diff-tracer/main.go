package main

import (
	"fmt"
	"io"
	"net/http"

	"os"

	"strings"

	"github.com/charmbracelet/lipgloss"

	"golang.org/x/term"
)

func main2() {
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

const columnWidth = 50

// Style definitions.
var (
	// General.

	normal  = lipgloss.Color("#EEEEEE")
	subtle  = lipgloss.AdaptiveColor{Light: "#D9DCCF", Dark: "#383838"}
	special = lipgloss.AdaptiveColor{Light: "#43BF6D", Dark: "#73F59F"}

	base = lipgloss.NewStyle().Foreground(normal)

	divider = lipgloss.NewStyle().
		SetString("•").
		Padding(0, 1).
		Foreground(subtle).
		String()

	url = lipgloss.NewStyle().Foreground(special).Render

	// Title.

	descStyle = base.MarginTop(1)

	infoStyle = base.
			BorderStyle(lipgloss.NormalBorder()).
			BorderTop(true).
			BorderForeground(subtle)

	// Paragraphs/History.

	codeBlockStyle = lipgloss.NewStyle().
			Align(lipgloss.Left).
			Foreground(lipgloss.Color("#FAFAFA")).
			Margin(1, 1, 0, 0).
			Padding(1, 2).
			Width(columnWidth).
			BorderStyle(lipgloss.NormalBorder()).
			BorderForeground(lipgloss.Color("63"))

	// Page.

	docStyle = lipgloss.NewStyle().Padding(1, 2, 1, 2)
)

func main() {
	physicalWidth, _, _ := term.GetSize(int(os.Stdout.Fd()))
	doc := strings.Builder{}

	// Title
	{
		var title strings.Builder

		desc := lipgloss.JoinVertical(lipgloss.Left,
			descStyle.Render("Style Definitions for Nice Terminal Layouts"),
			infoStyle.Render("From Charm"+divider+url("https://github.com/charmbracelet/lipgloss")),
		)

		row := lipgloss.JoinHorizontal(lipgloss.Top, title.String(), desc)
		doc.WriteString(row + "\n\n")
	}

	doc.WriteString(lipgloss.JoinHorizontal(lipgloss.Top))

	// code blocks
	{
		data := `{"data":[],"meta":{"numberOfUnreadNotifications":0,"total":0,"anotherArr":[1,2],"exists":false},hash:{}}`
		displayedCode1 := formatter(data)
		displayedCode2 := formatter(data)

		doc.WriteString(lipgloss.JoinHorizontal(
			lipgloss.Top,
			codeBlockStyle.Align(lipgloss.Left).Render(displayedCode1),
			codeBlockStyle.Align(lipgloss.Left).Render(displayedCode2),
		))

		doc.WriteString("\n\n")
	}

	var (
		// Status Bar.

		statusNugget = lipgloss.NewStyle().
				Padding(0, 1)

		statusBarStyle = lipgloss.NewStyle()

		equalLine = lipgloss.NewStyle().UnsetBackground()

		statusStyle = lipgloss.NewStyle().
				Background(lipgloss.Color("#b23655")).
				Padding(0, 1).
				MarginRight(1)

		encodingStyle = statusNugget.
				Background(lipgloss.Color("#347d39")).
				Align(lipgloss.Right)
	)

	{

		statusKey := statusStyle.Render("STATUS")
		encoding := encodingStyle.Render("UTF-8")

		bar := lipgloss.JoinVertical(
			lipgloss.Top,
			equalLine.Render("{"),
			statusKey,
			encoding,
			equalLine.Render("}"),
		)

		doc.WriteString(statusBarStyle.Width(96).Render(bar))
	}

	if physicalWidth > 0 {
		docStyle = docStyle.MaxWidth(physicalWidth)
	}

	// Okay, let's print it
	fmt.Println(docStyle.Render(doc.String()))
}
