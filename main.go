package main

import (
	"fmt"
	"os"

	dem "github.com/markus-wa/demoinfocs-golang/v2/pkg/demoinfocs"
	events "github.com/markus-wa/demoinfocs-golang/v2/pkg/demoinfocs/events"
)

func main() {
	f, err := os.Open("demo_csgo/dem_file/de_inferno_1677703808.dem")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	p := dem.NewParser(f)
	defer p.Close()

	// Register handler on kill events
	

	p.RegisterEventHandler(func(e events.Kill) {

		gs := p.GameState()
		var test = gs.IngameTick()

		
		fmt.Println(test)
	})

	// Parse to end
	err = p.ParseToEnd()
	if err != nil {
		panic(err)
	}
}