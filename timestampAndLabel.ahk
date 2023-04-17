#Requires AutoHotkey v2.0
#SingleInstance

; decide what to call your output folder
folderOfAudios := "audio-labelling"

; dont change anything past here unless you read the code
recording := False

Tooltip "timestampAndLabel.ahk launched"
Sleep 1000
Tooltip

if !(DirExist(A_WorkingDir "\" folderOfAudios)) {
    DirCreate(A_WorkingDir "\" folderOfAudios)
}
;
;  Functions
    justTime(d) {
        return SubStr(String(Number(d)),9,8)
    }
    justDate(d) {
        return SubStr(String(Number(d)),1,8)
    }

    secondsToStamp(s) {
        hour := Floor(s/3600) ""
        mins := Floor((s-(hour*3600))/60) ""
        secs := Floor((s-(hour*3600)-(mins*60))) ""
        if (StrLen(hour) == 1)
            hour := "0" hour
        if (StrLen(mins) == 1)
            mins := "0" mins
        if (StrLen(secs) == 1)
            secs := "0" secs
        return String(hour ":" mins ":" secs)
    }
;
;  Keybinds
    ^+!t::{
	global recording, recordingStartTime, txtFile
        if !(recording) {
            recordingStartTime := A_Now
            txtFile := A_WorkingDir "\" folderOfAudios "\" recordingStartTime ".txt"
            audioTitle := InputBox("Describe recording (optional)`r^+!t to make labels", "audio-labelling INIT","W210 H110").value
            if (audioTitle) {
                FileAppend String("`r" ">" audioTitle), txtFile
            }
            recording := True
        } else {
            stopTime := DateDiff(A_Now,recordingStartTime,"s")

            noInput := True
            While (noInput) {
                userText := InputBox("Describe section (required)", "audio-label END", "W100 H110").value
                try { 
                    if(userText) {
                        noInput := False
                    }
                }
            }
            
            FileAppend(String("`r" "$" secondsToStamp(stopTime) userText), txtFile)
        } 
    }
    ^+!n::{
        Reload
    }
;