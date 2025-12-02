#SingleInstance force  ; 同じスクリプトの古いインスタンスを強制終了

; コマンドライン引数に基づいてIMEの状態を設定する
if A_Args[1] == "IME_On" {
    IME_On()
} else if A_Args[1] == "IME_Off" {
    IME_Off()
}

;-----------------------------------------------------------
; IMEの状態をセット
;   SetSts          1:ON / 0:OFF
;   WinTitle="A"    対象Window
;   戻り値          0:成功 / 0以外:失敗
;-----------------------------------------------------------
IME_SET(SetSts, WinTitle:="A") {
    hwnd := WinExist(WinTitle)
    if (WinActive(WinTitle)) {
        ptrSize := A_PtrSize
        cbSize := 4 + 4 + (ptrSize * 6) + 16
        stGTI := Buffer(cbSize, 0)
        NumPut("UInt", cbSize, stGTI, 0)   ; DWORD cbSize;

        if (DllCall("GetGUIThreadInfo", "UInt", 0, "Ptr", stGTI)) {
            hwnd := NumGet(stGTI, 8 + ptrSize, "UInt")
        }
    }
    return DllCall("SendMessage"
          , "Ptr", DllCall("imm32\ImmGetDefaultIMEWnd", "Ptr", hwnd)
          , "UInt", 0x0283  ; Message: WM_IME_CONTROL
          , "Int", 0x006    ; wParam : IMC_SETOPENSTATUS
          , "Int", SetSts)  ; lParam : 0 or 1
}

; IMEをオンにする関数
IME_On() {
    IME_SET(1) ; IMEをオンにする
    ExitApp
}

; IMEをオフにする関数
IME_Off() {
    IME_SET(0) ; IMEをオフにする
    ExitApp
}
