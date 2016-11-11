from raphidoc import mdx_math
from raphidoc.exceptions import RaphidocException

import pytest

CACHE_DIRECTORY = 'tests/.cache/'


def test_svg_rewrite():
    svg = """<svg xmlns:xlink="http://www.w3.org/1999/xlink"
    width="4.65ex" height="3.676ex" style="vertical-align: -1.338ex;"
    viewBox="0 -1006.6 2002 1582.7" role="img" focusable="false"
    xmlns="http://www.w3.org/2000/svg">
    <defs>
    <path stroke-width="1" id="E1-MJMATHI-73" d="M131 289Q131 321 147 354T203 415T300 442Q362 442 390 415T419 355Q419 323 402 308T364 292Q351 292 340 300T328 326Q328 342 337 354T354 372T367 378Q368 378 368 379Q368 382 361 388T336 399T297 405Q249 405 227 379T204 326Q204 301 223 291T278 274T330 259Q396 230 396 163Q396 135 385 107T352 51T289 7T195 -10Q118 -10 86 19T53 87Q53 126 74 143T118 160Q133 160 146 151T160 120Q160 94 142 76T111 58Q109 57 108 57T107 55Q108 52 115 47T146 34T201 27Q237 27 263 38T301 66T318 97T323 122Q323 150 302 164T254 181T195 196T148 231Q131 256 131 289Z"></path>
    <path stroke-width="1" id="E1-MJMAIN-31" d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z"></path>
    <path stroke-width="1" id="E1-MJMAIN-32" d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z"></path>
    <path stroke-width="1" id="E1-MJMATHI-72" d="M21 287Q22 290 23 295T28 317T38 348T53 381T73 411T99 433T132 442Q161 442 183 430T214 408T225 388Q227 382 228 382T236 389Q284 441 347 441H350Q398 441 422 400Q430 381 430 363Q430 333 417 315T391 292T366 288Q346 288 334 299T322 328Q322 376 378 392Q356 405 342 405Q286 405 239 331Q229 315 224 298T190 165Q156 25 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 114 189T154 366Q154 405 128 405Q107 405 92 377T68 316T57 280Q55 278 41 278H27Q21 284 21 287Z"></path>
    </defs>
    <g stroke="currentColor" fill="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)">
        <g transform="translate(120,0)">
        <rect stroke="none" width="810" height="60" x="0" y="220"></rect>
        <g transform="translate(60,584)">
        <use transform="scale(0.707)" xlink:href="#E1-MJMATHI-73" x="0" y="0"></use>
        <use transform="scale(0.574)" xlink:href="#E1-MJMAIN-31" x="578" y="-243"></use>
        </g>
        <g transform="translate(60,-345)">
        <use transform="scale(0.707)" xlink:href="#E1-MJMATHI-73" x="0" y="0"></use>
        <use transform="scale(0.574)" xlink:href="#E1-MJMAIN-32" x="578" y="-243"></use>
        </g>
        </g>
        <use xlink:href="#E1-MJMATHI-72" x="1050" y="0"></use>
        <use xlink:href="#E1-MJMAIN-32" x="1501" y="0"></use>
    </g>
    </svg>
    """
    inlined = mdx_math.svg_rewrite(svg)
    assert inlined == """<svg focusable="false" height="3.676ex" role="img" style="vertical-align: -1.338ex;" viewBox="0 -1006.6 2002 1582.7" width="4.65ex">
    <g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)">
        <g transform="translate(120,0)">
        <rect height="60" stroke="none" width="810" x="0" y="220" />
        <g transform="translate(60,584)">
        <path d="M131 289Q131 321 147 354T203 415T300 442Q362 442 390 415T419 355Q419 323 402 308T364 292Q351 292 340 300T328 326Q328 342 337 354T354 372T367 378Q368 378 368 379Q368 382 361 388T336 399T297 405Q249 405 227 379T204 326Q204 301 223 291T278 274T330 259Q396 230 396 163Q396 135 385 107T352 51T289 7T195 -10Q118 -10 86 19T53 87Q53 126 74 143T118 160Q133 160 146 151T160 120Q160 94 142 76T111 58Q109 57 108 57T107 55Q108 52 115 47T146 34T201 27Q237 27 263 38T301 66T318 97T323 122Q323 150 302 164T254 181T195 196T148 231Q131 256 131 289Z" stroke-width="1" transform="scale(0.707)translate(0, 0)" />
        <path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" stroke-width="1" transform="scale(0.574)translate(578, -243)" />
        </g>
        <g transform="translate(60,-345)">
        <path d="M131 289Q131 321 147 354T203 415T300 442Q362 442 390 415T419 355Q419 323 402 308T364 292Q351 292 340 300T328 326Q328 342 337 354T354 372T367 378Q368 378 368 379Q368 382 361 388T336 399T297 405Q249 405 227 379T204 326Q204 301 223 291T278 274T330 259Q396 230 396 163Q396 135 385 107T352 51T289 7T195 -10Q118 -10 86 19T53 87Q53 126 74 143T118 160Q133 160 146 151T160 120Q160 94 142 76T111 58Q109 57 108 57T107 55Q108 52 115 47T146 34T201 27Q237 27 263 38T301 66T318 97T323 122Q323 150 302 164T254 181T195 196T148 231Q131 256 131 289Z" stroke-width="1" transform="scale(0.707)translate(0, 0)" />
        <path d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z" stroke-width="1" transform="scale(0.574)translate(578, -243)" />
        </g>
        </g>
        <path d="M21 287Q22 290 23 295T28 317T38 348T53 381T73 411T99 433T132 442Q161 442 183 430T214 408T225 388Q227 382 228 382T236 389Q284 441 347 441H350Q398 441 422 400Q430 381 430 363Q430 333 417 315T391 292T366 288Q346 288 334 299T322 328Q322 376 378 392Q356 405 342 405Q286 405 239 331Q229 315 224 298T190 165Q156 25 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 114 189T154 366Q154 405 128 405Q107 405 92 377T68 316T57 280Q55 278 41 278H27Q21 284 21 287Z" stroke-width="1" transform="translate(1050, 0)" />
        <path d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z" stroke-width="1" transform="translate(1501, 0)" />
    </g>
    </svg>"""


def test_run_in_node():
    program = 'console.log("Test me!");'
    assert mdx_math.run_in_node(program, CACHE_DIRECTORY) == "Test me!\n"


def test_run_in_node_on_error():
    program = 'lkasl1'
    with pytest.raises(RaphidocException) as excinfo:
        assert mdx_math.run_in_node(program, CACHE_DIRECTORY) == ""
    assert str(excinfo.value).split('\n', 1)[0] == "Failed to convert math formula via node."


def test_install_dependencies():
    # TODO: check for node_modules directory
    mdx_math.FAILED_INSTALLATION = False
    mdx_math.install_dependencies(CACHE_DIRECTORY)
    assert not mdx_math.FAILED_INSTALLATION


def test_compile_latex_with_mdx_error():
    try:
        mdx_math.FAILED_INSTALLATION = True
        assert '<span class="missing-formula">\sum_{i=1}^n i</span>' == mdx_math.compile_latex(
            '\sum_{i=1}^n i', True, CACHE_DIRECTORY, no_cache=True)
    finally:
        mdx_math.FAILED_INSTALLATION = False


def test_compile_latex_inline():
    assert mdx_math.compile_latex('\sum_{i=1}^n i', True, CACHE_DIRECTORY, no_cache=True) == """<svg focusable="false" height="3.176ex" role="img" style="vertical-align: -1.005ex;" viewBox="0 -934.9 2817.4 1367.4" width="6.544ex">
<g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)">
 <path d="M61 748Q64 750 489 750H913L954 640Q965 609 976 579T993 533T999 516H979L959 517Q936 579 886 621T777 682Q724 700 655 705T436 710H319Q183 710 183 709Q186 706 348 484T511 259Q517 250 513 244L490 216Q466 188 420 134T330 27L149 -187Q149 -188 362 -188Q388 -188 436 -188T506 -189Q679 -189 778 -162T936 -43Q946 -27 959 6H999L913 -249L489 -250Q65 -250 62 -248Q56 -246 56 -239Q56 -234 118 -161Q186 -81 245 -11L428 206Q428 207 242 462L57 717L56 728Q56 744 61 748Z" stroke-width="1" transform="translate(0, 0)" />
 <path d="M21 287Q22 293 24 303T36 341T56 388T89 425T135 442Q171 442 195 424T225 390T231 369Q231 367 232 367L243 378Q304 442 382 442Q436 442 469 415T503 336T465 179T427 52Q427 26 444 26Q450 26 453 27Q482 32 505 65T540 145Q542 153 560 153Q580 153 580 145Q580 144 576 130Q568 101 554 73T508 17T439 -10Q392 -10 371 17T350 73Q350 92 386 193T423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 180T152 343Q153 348 153 366Q153 405 129 405Q91 405 66 305Q60 285 60 284Q58 278 41 278H27Q21 284 21 287Z" stroke-width="1" transform="scale(0.707)translate(1494, 675)" />
<g transform="translate(1056,-287)">
 <path d="M184 600Q184 624 203 642T247 661Q265 661 277 649T290 619Q290 596 270 577T226 557Q211 557 198 567T184 600ZM21 287Q21 295 30 318T54 369T98 420T158 442Q197 442 223 419T250 357Q250 340 236 301T196 196T154 83Q149 61 149 51Q149 26 166 26Q175 26 185 29T208 43T235 78T260 137Q263 149 265 151T282 153Q302 153 302 143Q302 135 293 112T268 61T223 11T161 -11Q129 -11 102 10T74 74Q74 91 79 106T122 220Q160 321 166 341T173 380Q173 404 156 404H154Q124 404 99 371T61 287Q60 286 59 284T58 281T56 279T53 278T49 278T41 278H27Q21 284 21 287Z" stroke-width="1" transform="scale(0.707)translate(0, 0)" />
 <path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" stroke-width="1" transform="scale(0.707)translate(345, 0)" />
 <path d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z" stroke-width="1" transform="scale(0.707)translate(1124, 0)" />
</g>
 <path d="M184 600Q184 624 203 642T247 661Q265 661 277 649T290 619Q290 596 270 577T226 557Q211 557 198 567T184 600ZM21 287Q21 295 30 318T54 369T98 420T158 442Q197 442 223 419T250 357Q250 340 236 301T196 196T154 83Q149 61 149 51Q149 26 166 26Q175 26 185 29T208 43T235 78T260 137Q263 149 265 151T282 153Q302 153 302 143Q302 135 293 112T268 61T223 11T161 -11Q129 -11 102 10T74 74Q74 91 79 106T122 220Q160 321 166 341T173 380Q173 404 156 404H154Q124 404 99 371T61 287Q60 286 59 284T58 281T56 279T53 278T49 278T41 278H27Q21 284 21 287Z" stroke-width="1" transform="translate(2471, 0)" />
</g>
</svg>"""


def test_compile_latex_excaped():
    assert mdx_math.compile_latex('"Break', False, CACHE_DIRECTORY, no_cache=True) == """<svg focusable="false" height="2.176ex" role="img" style="vertical-align: -0.338ex;" viewBox="0 -791.3 3506.8 936.9" width="8.145ex">
<g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)">
 <path d="M34 634Q34 659 50 676T93 694Q121 694 144 668T168 579Q168 525 146 476T101 403T73 379Q69 379 60 388T50 401Q50 404 62 417T88 448T116 500T131 572Q131 584 130 584T125 581T112 576T94 573Q69 573 52 590T34 634ZM238 634Q238 659 254 676T297 694Q325 694 348 668T372 579Q372 525 350 476T305 403T277 379Q273 379 264 388T254 401Q254 404 266 417T292 448T320 500T335 572Q335 584 334 584T329 581T316 576T298 573Q273 573 256 590T238 634Z" stroke-width="1" transform="translate(0, 0)" />
 <path d="M231 637Q204 637 199 638T194 649Q194 676 205 682Q206 683 335 683Q594 683 608 681Q671 671 713 636T756 544Q756 480 698 429T565 360L555 357Q619 348 660 311T702 219Q702 146 630 78T453 1Q446 0 242 0Q42 0 39 2Q35 5 35 10Q35 17 37 24Q42 43 47 45Q51 46 62 46H68Q95 46 128 49Q142 52 147 61Q150 65 219 339T288 628Q288 635 231 637ZM649 544Q649 574 634 600T585 634Q578 636 493 637Q473 637 451 637T416 636H403Q388 635 384 626Q382 622 352 506Q352 503 351 500L320 374H401Q482 374 494 376Q554 386 601 434T649 544ZM595 229Q595 273 572 302T512 336Q506 337 429 337Q311 337 310 336Q310 334 293 263T258 122L240 52Q240 48 252 48T333 46Q422 46 429 47Q491 54 543 105T595 229Z" stroke-width="1" transform="translate(778, 0)" />
 <path d="M21 287Q22 290 23 295T28 317T38 348T53 381T73 411T99 433T132 442Q161 442 183 430T214 408T225 388Q227 382 228 382T236 389Q284 441 347 441H350Q398 441 422 400Q430 381 430 363Q430 333 417 315T391 292T366 288Q346 288 334 299T322 328Q322 376 378 392Q356 405 342 405Q286 405 239 331Q229 315 224 298T190 165Q156 25 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 114 189T154 366Q154 405 128 405Q107 405 92 377T68 316T57 280Q55 278 41 278H27Q21 284 21 287Z" stroke-width="1" transform="translate(1537, 0)" />
 <path d="M39 168Q39 225 58 272T107 350T174 402T244 433T307 442H310Q355 442 388 420T421 355Q421 265 310 237Q261 224 176 223Q139 223 138 221Q138 219 132 186T125 128Q125 81 146 54T209 26T302 45T394 111Q403 121 406 121Q410 121 419 112T429 98T420 82T390 55T344 24T281 -1T205 -11Q126 -11 83 42T39 168ZM373 353Q367 405 305 405Q272 405 244 391T199 357T170 316T154 280T149 261Q149 260 169 260Q282 260 327 284T373 353Z" stroke-width="1" transform="translate(1989, 0)" />
 <path d="M33 157Q33 258 109 349T280 441Q331 441 370 392Q386 422 416 422Q429 422 439 414T449 394Q449 381 412 234T374 68Q374 43 381 35T402 26Q411 27 422 35Q443 55 463 131Q469 151 473 152Q475 153 483 153H487Q506 153 506 144Q506 138 501 117T481 63T449 13Q436 0 417 -8Q409 -10 393 -10Q359 -10 336 5T306 36L300 51Q299 52 296 50Q294 48 292 46Q233 -10 172 -10Q117 -10 75 30T33 157ZM351 328Q351 334 346 350T323 385T277 405Q242 405 210 374T160 293Q131 214 119 129Q119 126 119 118T118 106Q118 61 136 44T179 26Q217 26 254 59T298 110Q300 114 325 217T351 328Z" stroke-width="1" transform="translate(2455, 0)" />
 <path d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z" stroke-width="1" transform="translate(2985, 0)" />
</g>
</svg>"""


def test_compile_latex():
    assert mdx_math.compile_latex('e=mc^2', False, CACHE_DIRECTORY, no_cache=True) == """<svg focusable="false" height="2.676ex" role="img" style="vertical-align: -0.338ex;" viewBox="0 -1006.6 3566.5 1152.1" width="8.283ex">
<g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)">
 <path d="M39 168Q39 225 58 272T107 350T174 402T244 433T307 442H310Q355 442 388 420T421 355Q421 265 310 237Q261 224 176 223Q139 223 138 221Q138 219 132 186T125 128Q125 81 146 54T209 26T302 45T394 111Q403 121 406 121Q410 121 419 112T429 98T420 82T390 55T344 24T281 -1T205 -11Q126 -11 83 42T39 168ZM373 353Q367 405 305 405Q272 405 244 391T199 357T170 316T154 280T149 261Q149 260 169 260Q282 260 327 284T373 353Z" stroke-width="1" transform="translate(0, 0)" />
 <path d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z" stroke-width="1" transform="translate(744, 0)" />
 <path d="M21 287Q22 293 24 303T36 341T56 388T88 425T132 442T175 435T205 417T221 395T229 376L231 369Q231 367 232 367L243 378Q303 442 384 442Q401 442 415 440T441 433T460 423T475 411T485 398T493 385T497 373T500 364T502 357L510 367Q573 442 659 442Q713 442 746 415T780 336Q780 285 742 178T704 50Q705 36 709 31T724 26Q752 26 776 56T815 138Q818 149 821 151T837 153Q857 153 857 145Q857 144 853 130Q845 101 831 73T785 17T716 -10Q669 -10 648 17T627 73Q627 92 663 193T700 345Q700 404 656 404H651Q565 404 506 303L499 291L466 157Q433 26 428 16Q415 -11 385 -11Q372 -11 364 -4T353 8T350 18Q350 29 384 161L420 307Q423 322 423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 181Q151 335 151 342Q154 357 154 369Q154 405 129 405Q107 405 92 377T69 316T57 280Q55 278 41 278H27Q21 284 21 287Z" stroke-width="1" transform="translate(1800, 0)" />
<g transform="translate(2679,0)">
 <path d="M34 159Q34 268 120 355T306 442Q362 442 394 418T427 355Q427 326 408 306T360 285Q341 285 330 295T319 325T330 359T352 380T366 386H367Q367 388 361 392T340 400T306 404Q276 404 249 390Q228 381 206 359Q162 315 142 235T121 119Q121 73 147 50Q169 26 205 26H209Q321 26 394 111Q403 121 406 121Q410 121 419 112T429 98T420 83T391 55T346 25T282 0T202 -11Q127 -11 81 37T34 159Z" stroke-width="1" transform="translate(0, 0)" />
 <path d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z" stroke-width="1" transform="scale(0.707)translate(613, 583)" />
</g>
</g>
</svg>"""


def test_compile_latex_error():
    print(mdx_math.compile_latex('e^^', False, CACHE_DIRECTORY, no_cache=True))
    assert mdx_math.compile_latex('e^^', False, CACHE_DIRECTORY, no_cache=True) == """<svg focusable="false" height="4.509ex" role="img" style="vertical-align: -1.838ex;" viewBox="-5 -1150.1 19248.6 1941.5" width="44.707ex">
<g fill="currentColor" stroke="currentColor" stroke-width="0" transform="matrix(1 0 0 -1 0 0)">
<rect fill="rgb(255, 255, 136)" height="1736" stroke="none" width="19238" x="0" y="-675" />
<g fill="rgb(204, 0, 0)" stroke="rgb(204, 0, 0)" transform="translate(287,0)">
<g transform="scale(0.9)">
<text direction="ltr" font-family="monospace" stroke="none" transform="scale(71.759) matrix(1 0 0 -1 0 0)">Missing open brace for superscript</text>
</g>
</g>
<line stroke="#c00" stroke-linecap="square" stroke-width="71.76" transform="translate(-5,-675)" x1="35" x2="35" y1="35" y2="1700" />
<line stroke="#c00" stroke-linecap="square" stroke-width="71.76" transform="translate(19171,-675)" x1="35" x2="35" y1="35" y2="1700" />
<line stroke="#c00" stroke-linecap="square" stroke-width="71.76" transform="translate(0,995)" x1="35" x2="19202" y1="35" y2="35" />
<line stroke="#c00" stroke-linecap="square" stroke-width="71.76" transform="translate(0,-680)" x1="35" x2="19202" y1="35" y2="35" />
</g>
</svg>"""
