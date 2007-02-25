_types = {
     0 : 'EV_SYN',
     1 : 'EV_KEY',
     2 : 'EV_REL',
     3 : 'EV_ABS',
     4 : 'EV_MSC',
     5 : 'EV_SW',
    17 : 'EV_LED',
    18 : 'EV_SND',
    20 : 'EV_REP',
    21 : 'EV_FF',
    22 : 'EV_PWR',
    23 : 'EV_FF_STATUS',
    31 : 'EV_MAX',
}

_events = {
    0 : { # EV_SYN
          0 : 'SYN_REPORT',
          1 : 'SYN_CONFIG',
    },
    1 : { # EV_KEY
          0 : 'KEY_RESERVED',
          1 : 'KEY_ESC',
          2 : 'KEY_1',
          3 : 'KEY_2',
          4 : 'KEY_3',
          5 : 'KEY_4',
          6 : 'KEY_5',
          7 : 'KEY_6',
          8 : 'KEY_7',
          9 : 'KEY_8',
         10 : 'KEY_9',
         11 : 'KEY_0',
         12 : 'KEY_MINUS',
         13 : 'KEY_EQUAL',
         14 : 'KEY_BACKSPACE',
         15 : 'KEY_TAB',
         16 : 'KEY_Q',
         17 : 'KEY_W',
         18 : 'KEY_E',
         19 : 'KEY_R',
         20 : 'KEY_T',
         21 : 'KEY_Y',
         22 : 'KEY_U',
         23 : 'KEY_I',
         24 : 'KEY_O',
         25 : 'KEY_P',
         26 : 'KEY_LEFTBRACE',
         27 : 'KEY_RIGHTBRACE',
         28 : 'KEY_ENTER',
         29 : 'KEY_LEFTCTRL',
         30 : 'KEY_A',
         31 : 'KEY_S',
         32 : 'KEY_D',
         33 : 'KEY_F',
         34 : 'KEY_G',
         35 : 'KEY_H',
         36 : 'KEY_J',
         37 : 'KEY_K',
         38 : 'KEY_L',
         39 : 'KEY_SEMICOLON',
         40 : 'KEY_APOSTROPHE',
         41 : 'KEY_GRAVE',
         42 : 'KEY_LEFTSHIFT',
         43 : 'KEY_BACKSLASH',
         44 : 'KEY_Z',
         45 : 'KEY_X',
         46 : 'KEY_C',
         47 : 'KEY_V',
         48 : 'KEY_B',
         49 : 'KEY_N',
         50 : 'KEY_M',
         51 : 'KEY_COMMA',
         52 : 'KEY_DOT',
         53 : 'KEY_SLASH',
         54 : 'KEY_RIGHTSHIFT',
         55 : 'KEY_KPASTERISK',
         56 : 'KEY_LEFTALT',
         57 : 'KEY_SPACE',
         58 : 'KEY_CAPSLOCK',
         59 : 'KEY_F1',
         60 : 'KEY_F2',
         61 : 'KEY_F3',
         62 : 'KEY_F4',
         63 : 'KEY_F5',
         64 : 'KEY_F6',
         65 : 'KEY_F7',
         66 : 'KEY_F8',
         67 : 'KEY_F9',
         68 : 'KEY_F10',
         69 : 'KEY_NUMLOCK',
         70 : 'KEY_SCROLLLOCK',
         71 : 'KEY_KP7',
         72 : 'KEY_KP8',
         73 : 'KEY_KP9',
         74 : 'KEY_KPMINUS',
         75 : 'KEY_KP4',
         76 : 'KEY_KP5',
         77 : 'KEY_KP6',
         78 : 'KEY_KPPLUS',
         79 : 'KEY_KP1',
         80 : 'KEY_KP2',
         81 : 'KEY_KP3',
         82 : 'KEY_KP0',
         83 : 'KEY_KPDOT',
         85 : 'KEY_ZENKAKUHANKAKU',
         86 : 'KEY_102ND',
         87 : 'KEY_F11',
         88 : 'KEY_F12',
         89 : 'KEY_RO',
         90 : 'KEY_KATAKANA',
         91 : 'KEY_HIRAGANA',
         92 : 'KEY_HENKAN',
         93 : 'KEY_KATAKANAHIRAGANA',
         94 : 'KEY_MUHENKAN',
         95 : 'KEY_KPJPCOMMA',
         96 : 'KEY_KPENTER',
         97 : 'KEY_RIGHTCTRL',
         98 : 'KEY_KPSLASH',
         99 : 'KEY_SYSRQ',
        100 : 'KEY_RIGHTALT',
        101 : 'KEY_LINEFEED',
        102 : 'KEY_HOME',
        103 : 'KEY_UP',
        104 : 'KEY_PAGEUP',
        105 : 'KEY_LEFT',
        106 : 'KEY_RIGHT',
        107 : 'KEY_END',
        108 : 'KEY_DOWN',
        109 : 'KEY_PAGEDOWN',
        110 : 'KEY_INSERT',
        111 : 'KEY_DELETE',
        112 : 'KEY_MACRO',
        113 : 'KEY_MUTE',
        114 : 'KEY_VOLUMEDOWN',
        115 : 'KEY_VOLUMEUP',
        116 : 'KEY_POWER',
        117 : 'KEY_KPEQUAL',
        118 : 'KEY_KPPLUSMINUS',
        119 : 'KEY_PAUSE',
        121 : 'KEY_KPCOMMA',
        122 : 'KEY_HANGEUL',
        123 : 'KEY_HANJA',
        124 : 'KEY_YEN',
        125 : 'KEY_LEFTMETA',
        126 : 'KEY_RIGHTMETA',
        127 : 'KEY_COMPOSE',
        128 : 'KEY_STOP',
        129 : 'KEY_AGAIN',
        130 : 'KEY_PROPS',
        131 : 'KEY_UNDO',
        132 : 'KEY_FRONT',
        133 : 'KEY_COPY',
        134 : 'KEY_OPEN',
        135 : 'KEY_PASTE',
        136 : 'KEY_FIND',
        137 : 'KEY_CUT',
        138 : 'KEY_HELP',
        139 : 'KEY_MENU',
        140 : 'KEY_CALC',
        141 : 'KEY_SETUP',
        142 : 'KEY_SLEEP',
        143 : 'KEY_WAKEUP',
        144 : 'KEY_FILE',
        145 : 'KEY_SENDFILE',
        146 : 'KEY_DELETEFILE',
        147 : 'KEY_XFER',
        148 : 'KEY_PROG1',
        149 : 'KEY_PROG2',
        150 : 'KEY_WWW',
        151 : 'KEY_MSDOS',
        152 : 'KEY_COFFEE',
        153 : 'KEY_DIRECTION',
        154 : 'KEY_CYCLEWINDOWS',
        155 : 'KEY_MAIL',
        156 : 'KEY_BOOKMARKS',
        157 : 'KEY_COMPUTER',
        158 : 'KEY_BACK',
        159 : 'KEY_FORWARD',
        160 : 'KEY_CLOSECD',
        161 : 'KEY_EJECTCD',
        162 : 'KEY_EJECTCLOSECD',
        163 : 'KEY_NEXTSONG',
        164 : 'KEY_PLAYPAUSE',
        165 : 'KEY_PREVIOUSSONG',
        166 : 'KEY_STOPCD',
        167 : 'KEY_RECORD',
        168 : 'KEY_REWIND',
        169 : 'KEY_PHONE',
        170 : 'KEY_ISO',
        171 : 'KEY_CONFIG',
        172 : 'KEY_HOMEPAGE',
        173 : 'KEY_REFRESH',
        174 : 'KEY_EXIT',
        175 : 'KEY_MOVE',
        176 : 'KEY_EDIT',
        177 : 'KEY_SCROLLUP',
        178 : 'KEY_SCROLLDOWN',
        179 : 'KEY_KPLEFTPAREN',
        180 : 'KEY_KPRIGHTPAREN',
        181 : 'KEY_NEW',
        182 : 'KEY_REDO',
        183 : 'KEY_F13',
        184 : 'KEY_F14',
        185 : 'KEY_F15',
        186 : 'KEY_F16',
        187 : 'KEY_F17',
        188 : 'KEY_F18',
        189 : 'KEY_F19',
        190 : 'KEY_F20',
        191 : 'KEY_F21',
        192 : 'KEY_F22',
        193 : 'KEY_F23',
        194 : 'KEY_F24',
        200 : 'KEY_PLAYCD',
        201 : 'KEY_PAUSECD',
        202 : 'KEY_PROG3',
        203 : 'KEY_PROG4',
        205 : 'KEY_SUSPEND',
        206 : 'KEY_CLOSE',
        207 : 'KEY_PLAY',
        208 : 'KEY_FASTFORWARD',
        209 : 'KEY_BASSBOOST',
        210 : 'KEY_PRINT',
        211 : 'KEY_HP',
        212 : 'KEY_CAMERA',
        213 : 'KEY_SOUND',
        214 : 'KEY_QUESTION',
        215 : 'KEY_EMAIL',
        216 : 'KEY_CHAT',
        217 : 'KEY_SEARCH',
        218 : 'KEY_CONNECT',
        219 : 'KEY_FINANCE',
        220 : 'KEY_SPORT',
        221 : 'KEY_SHOP',
        222 : 'KEY_ALTERASE',
        223 : 'KEY_CANCEL',
        224 : 'KEY_BRIGHTNESSDOWN',
        225 : 'KEY_BRIGHTNESSUP',
        226 : 'KEY_MEDIA',
        227 : 'KEY_SWITCHVIDEOMODE',
        228 : 'KEY_KBDILLUMTOGGLE',
        229 : 'KEY_KBDILLUMDOWN',
        230 : 'KEY_KBDILLUMUP',
        231 : 'KEY_SEND',
        232 : 'KEY_REPLY',
        233 : 'KEY_FORWARDMAIL',
        234 : 'KEY_SAVE',
        235 : 'KEY_DOCUMENTS',
        236 : 'KEY_BATTERY',
        240 : 'KEY_UNKNOWN',
        256 : 'BTN_0',
        257 : 'BTN_1',
        258 : 'BTN_2',
        259 : 'BTN_3',
        260 : 'BTN_4',
        261 : 'BTN_5',
        262 : 'BTN_6',
        263 : 'BTN_7',
        264 : 'BTN_8',
        265 : 'BTN_9',
        272 : 'BTN_LEFT',
        273 : 'BTN_RIGHT',
        274 : 'BTN_MIDDLE',
        275 : 'BTN_SIDE',
        276 : 'BTN_EXTRA',
        277 : 'BTN_FORWARD',
        278 : 'BTN_BACK',
        279 : 'BTN_TASK',
        288 : 'BTN_TRIGGER',
        289 : 'BTN_THUMB',
        290 : 'BTN_THUMB2',
        291 : 'BTN_TOP',
        292 : 'BTN_TOP2',
        293 : 'BTN_PINKIE',
        294 : 'BTN_BASE',
        295 : 'BTN_BASE2',
        296 : 'BTN_BASE3',
        297 : 'BTN_BASE4',
        298 : 'BTN_BASE5',
        299 : 'BTN_BASE6',
        303 : 'BTN_DEAD',
        304 : 'BTN_A',
        305 : 'BTN_B',
        306 : 'BTN_C',
        307 : 'BTN_X',
        308 : 'BTN_Y',
        309 : 'BTN_Z',
        310 : 'BTN_TL',
        311 : 'BTN_TR',
        312 : 'BTN_TL2',
        313 : 'BTN_TR2',
        314 : 'BTN_SELECT',
        315 : 'BTN_START',
        316 : 'BTN_MODE',
        317 : 'BTN_THUMBL',
        318 : 'BTN_THUMBR',
        320 : 'BTN_TOOL_PEN',
        321 : 'BTN_TOOL_RUBBER',
        322 : 'BTN_TOOL_BRUSH',
        323 : 'BTN_TOOL_PENCIL',
        324 : 'BTN_TOOL_AIRBRUSH',
        325 : 'BTN_TOOL_FINGER',
        326 : 'BTN_TOOL_MOUSE',
        327 : 'BTN_TOOL_LENS',
        330 : 'BTN_TOUCH',
        331 : 'BTN_STYLUS',
        332 : 'BTN_STYLUS2',
        333 : 'BTN_TOOL_DOUBLETAP',
        334 : 'BTN_TOOL_TRIPLETAP',
        336 : 'BTN_GEAR_DOWN',
        337 : 'BTN_GEAR_UP',
        352 : 'KEY_OK',
        353 : 'KEY_SELECT',
        354 : 'KEY_GOTO',
        355 : 'KEY_CLEAR',
        356 : 'KEY_POWER2',
        357 : 'KEY_OPTION',
        358 : 'KEY_INFO',
        359 : 'KEY_TIME',
        360 : 'KEY_VENDOR',
        361 : 'KEY_ARCHIVE',
        362 : 'KEY_PROGRAM',
        363 : 'KEY_CHANNEL',
        364 : 'KEY_FAVORITES',
        365 : 'KEY_EPG',
        366 : 'KEY_PVR',
        367 : 'KEY_MHP',
        368 : 'KEY_LANGUAGE',
        369 : 'KEY_TITLE',
        370 : 'KEY_SUBTITLE',
        371 : 'KEY_ANGLE',
        372 : 'KEY_ZOOM',
        373 : 'KEY_MODE',
        374 : 'KEY_KEYBOARD',
        375 : 'KEY_SCREEN',
        376 : 'KEY_PC',
        377 : 'KEY_TV',
        378 : 'KEY_TV2',
        379 : 'KEY_VCR',
        380 : 'KEY_VCR2',
        381 : 'KEY_SAT',
        382 : 'KEY_SAT2',
        383 : 'KEY_CD',
        384 : 'KEY_TAPE',
        385 : 'KEY_RADIO',
        386 : 'KEY_TUNER',
        387 : 'KEY_PLAYER',
        388 : 'KEY_TEXT',
        389 : 'KEY_DVD',
        390 : 'KEY_AUX',
        391 : 'KEY_MP3',
        392 : 'KEY_AUDIO',
        393 : 'KEY_VIDEO',
        394 : 'KEY_DIRECTORY',
        395 : 'KEY_LIST',
        396 : 'KEY_MEMO',
        397 : 'KEY_CALENDAR',
        398 : 'KEY_RED',
        399 : 'KEY_GREEN',
        400 : 'KEY_YELLOW',
        401 : 'KEY_BLUE',
        402 : 'KEY_CHANNELUP',
        403 : 'KEY_CHANNELDOWN',
        404 : 'KEY_FIRST',
        405 : 'KEY_LAST',
        406 : 'KEY_AB',
        407 : 'KEY_NEXT',
        408 : 'KEY_RESTART',
        409 : 'KEY_SLOW',
        410 : 'KEY_SHUFFLE',
        411 : 'KEY_BREAK',
        412 : 'KEY_PREVIOUS',
        413 : 'KEY_DIGITS',
        414 : 'KEY_TEEN',
        415 : 'KEY_TWEN',
        448 : 'KEY_DEL_EOL',
        449 : 'KEY_DEL_EOS',
        450 : 'KEY_INS_LINE',
        451 : 'KEY_DEL_LINE',
        464 : 'KEY_FN',
        465 : 'KEY_FN_ESC',
        466 : 'KEY_FN_F1',
        467 : 'KEY_FN_F2',
        468 : 'KEY_FN_F3',
        469 : 'KEY_FN_F4',
        470 : 'KEY_FN_F5',
        471 : 'KEY_FN_F6',
        472 : 'KEY_FN_F7',
        473 : 'KEY_FN_F8',
        474 : 'KEY_FN_F9',
        475 : 'KEY_FN_F10',
        476 : 'KEY_FN_F11',
        477 : 'KEY_FN_F12',
        478 : 'KEY_FN_1',
        479 : 'KEY_FN_2',
        480 : 'KEY_FN_D',
        481 : 'KEY_FN_E',
        482 : 'KEY_FN_F',
        483 : 'KEY_FN_S',
        484 : 'KEY_FN_B',
        497 : 'KEY_BRL_DOT1',
        498 : 'KEY_BRL_DOT2',
        499 : 'KEY_BRL_DOT3',
        500 : 'KEY_BRL_DOT4',
        501 : 'KEY_BRL_DOT5',
        502 : 'KEY_BRL_DOT6',
        503 : 'KEY_BRL_DOT7',
        504 : 'KEY_BRL_DOT8',
        511 : 'KEY_MAX',
    },
    2 : { # EV_REL
          0 : 'REL_X',
          1 : 'REL_Y',
          2 : 'REL_Z',
          3 : 'REL_RX',
          4 : 'REL_RY',
          5 : 'REL_RZ',
          6 : 'REL_HWHEEL',
          7 : 'REL_DIAL',
          8 : 'REL_WHEEL',
          9 : 'REL_MISC',
         15 : 'REL_MAX',
    },
    3 : { # EV_ABS
          0 : 'ABS_X',
          1 : 'ABS_Y',
          2 : 'ABS_Z',
          3 : 'ABS_RX',
          4 : 'ABS_RY',
          5 : 'ABS_RZ',
          6 : 'ABS_THROTTLE',
          7 : 'ABS_RUDDER',
          8 : 'ABS_WHEEL',
          9 : 'ABS_GAS',
         10 : 'ABS_BRAKE',
         16 : 'ABS_HAT0X',
         17 : 'ABS_HAT0Y',
         18 : 'ABS_HAT1X',
         19 : 'ABS_HAT1Y',
         20 : 'ABS_HAT2X',
         21 : 'ABS_HAT2Y',
         22 : 'ABS_HAT3X',
         23 : 'ABS_HAT3Y',
         24 : 'ABS_PRESSURE',
         25 : 'ABS_DISTANCE',
         26 : 'ABS_TILT_X',
         27 : 'ABS_TILT_Y',
         28 : 'ABS_TOOL_WIDTH',
         32 : 'ABS_VOLUME',
         40 : 'ABS_MISC',
         63 : 'ABS_MAX',
    },
    4 : { # EV_MSC
          0 : 'MSC_SERIAL',
          1 : 'MSC_PULSELED',
          2 : 'MSC_GESTURE',
          3 : 'MSC_RAW',
          4 : 'MSC_SCAN',
          7 : 'MSC_MAX',
    },
    5 : { # EV_SW
          0 : 'SW_LID',
          1 : 'SW_TABLET_MODE',
          2 : 'SW_HEADPHONE_INSERT',
         15 : 'SW_MAX',
    },
    17 : { # EV_LED
          0 : 'LED_NUML',
          1 : 'LED_CAPSL',
          2 : 'LED_SCROLLL',
          3 : 'LED_COMPOSE',
          4 : 'LED_KANA',
          5 : 'LED_SLEEP',
          6 : 'LED_SUSPEND',
          7 : 'LED_MUTE',
          8 : 'LED_MISC',
          9 : 'LED_MAIL',
         10 : 'LED_CHARGING',
         15 : 'LED_MAX',
    },
    18 : { # EV_SND
          0 : 'SND_CLICK',
          1 : 'SND_BELL',
          2 : 'SND_TONE',
          7 : 'SND_MAX',
    },
    20 : { # EV_REP
          0 : 'REP_DELAY',
          1 : 'REP_MAX',
    },
    21 : { # EV_FF
          0 : 'FF_STATUS_STOPPED',
          1 : 'FF_STATUS_MAX',
         97 : 'FF_AUTOCENTER',
         96 : 'FF_GAIN',
         80 : 'FF_RUMBLE',
         81 : 'FF_PERIODIC',
         82 : 'FF_CONSTANT',
         83 : 'FF_SPRING',
         84 : 'FF_FRICTION',
         85 : 'FF_DAMPER',
         86 : 'FF_INERTIA',
         87 : 'FF_RAMP',
         88 : 'FF_SQUARE',
         89 : 'FF_TRIANGLE',
         90 : 'FF_SINE',
         91 : 'FF_SAW_UP',
         92 : 'FF_SAW_DOWN',
         93 : 'FF_CUSTOM',
        127 : 'FF_MAX',
    },
}

_ids = {
     0 : 'ID_BUS',
     1 : 'ID_VENDOR',
     2 : 'ID_PRODUCT',
     3 : 'ID_VERSION',
}

_buses = {
     1 : 'BUS_PCI',
     2 : 'BUS_ISAPNP',
     3 : 'BUS_USB',
     4 : 'BUS_HIL',
     5 : 'BUS_BLUETOOTH',
    16 : 'BUS_ISA',
    17 : 'BUS_I8042',
    18 : 'BUS_XTKBD',
    19 : 'BUS_RS232',
    20 : 'BUS_GAMEPORT',
    21 : 'BUS_PARPORT',
    22 : 'BUS_AMIGA',
    23 : 'BUS_ADB',
    24 : 'BUS_I2C',
    25 : 'BUS_HOST',
    26 : 'BUS_GSC',
}
