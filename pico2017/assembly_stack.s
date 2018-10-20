foo:
    pushl %ebp              ; -4
    mov %esp, %ebp
    pushl %edi              ; -4
    pushl %esi              ; -4
    pushl %ebx              ; -4
    sub $0xf8, %esp         ; -0xf8
    movl $0x1, (%esp)       ; 
    movl $0x2, 0x4(%esp)
    movl $0x3, 0x8(%esp)
    movl $0x4, 0xc(%esp)

; 12(dec) = 0x0c
