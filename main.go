package main

import (
	"fmt"
	"os"

	dem "github.com/markus-wa/demoinfocs-golang/v2/pkg/demoinfocs"
	events "github.com/markus-wa/demoinfocs-golang/v2/pkg/demoinfocs/events"
)

type GameRound struct {
	RoundNum             int64              `json:"roundNum"`
	StartTick            int64              `json:"startTick"`
	Reason               string             `json:"roundEndReason"`
}

func convertRoundEndReason(r events.RoundEndReason) string {
	switch reason := r; reason {
	case 1:
		return "TargetBombed"
	case 2:
		return "VIPEscaped"
	case 3:
		return "VIPKilled"
	case 4:
		return "TerroristsEscaped"
	case 5:
		return "CTStoppedEscape"
	case 6:
		return "TerroristsStopped"
	case 7:
		return "BombDefused"
	case 8:
		return "CTWin"
	case 9:
		return "TerroristsWin"
	case 10:
		return "Draw"
	case 11:
		return "HostagesRescued"
	case 12:
		return "TargetSaved"
	case 13:
		return "HostagesNotRescued"
	case 14:
		return "TerroristsNotEscaped"
	case 15:
		return "VIPNotEscaped"
	case 16:
		return "GameStart"
	case 17:
		return "TerroristsSurrender"
	case 18:
		return "CTSurrender"
	default:
		return "Unknown"
	}
}

func main() {
	f, err := os.Open("demo_csgo/dem_file/de_inferno_1677703808.dem")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	p := dem.NewParser(f)
	defer p.Close()

	currentRound := GameRound{}
	// Register handler on kill events
	cpt := []int {}
	cpt2 := []int {}
	
	p.RegisterEventHandler(func(e events.RoundStart) {
		
		gs := p.GameState()
		cpt = append(cpt,len(cpt)+1)

		currentRound.RoundNum = int64(len(cpt) + 1)
		currentRound.StartTick = int64(gs.IngameTick())

		
		fmt.Println("start", convertRoundEndReason(e.Reason))
	})


	p.RegisterEventHandler(func(e events.RoundEnd) {
		cpt2 = append(cpt2,len(cpt)+1)
		currentRound.Reason = convertRoundEndReason(e.Reason)
		
	})
	

	// Parse to end
	err = p.ParseToEnd()
	if err != nil {
		panic(err)
	}
}