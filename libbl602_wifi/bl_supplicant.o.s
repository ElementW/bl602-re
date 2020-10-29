
libbl602_wifi/bl_supplicant.o:     file format elf32-littleriscv


Disassembly of section .text.supplicantRestoreDefaults:

00000000 <supplicantRestoreDefaults>:
   0:	1141                	addi	sp,sp,-16
   2:	c606                	sw	ra,12(sp)
   4:	c422                	sw	s0,8(sp)
   6:	c226                	sw	s1,4(sp)
   8:	c04a                	sw	s2,0(sp)

0000000a <.LBB25>:
   a:	44b00937          	lui	s2,0x44b00
   e:	12092583          	lw	a1,288(s2) # 44b00120 <.LASF751+0x44afd4a2>

00000012 <.LBE25>:
  12:	3e800413          	li	s0,1000
  16:	000004b7          	lui	s1,0x0
			16: R_RISCV_HI20	.LANCHOR0
			16: R_RISCV_RELAX	*ABS*
  1a:	0285d5b3          	divu	a1,a1,s0
  1e:	00000537          	lui	a0,0x0
			1e: R_RISCV_HI20	.LC0
			1e: R_RISCV_RELAX	*ABS*
  22:	00048613          	mv	a2,s1
			22: R_RISCV_LO12_I	.LANCHOR0
			22: R_RISCV_RELAX	*ABS*
  26:	00050513          	mv	a0,a0
			26: R_RISCV_LO12_I	.LC0
			26: R_RISCV_RELAX	*ABS*
  2a:	00000097          	auipc	ra,0x0
			2a: R_RISCV_CALL	dbg_test_print
			2a: R_RISCV_RELAX	*ABS*
  2e:	000080e7          	jalr	ra # 2a <.LBE25+0x18>

00000032 <.LVL0>:
  32:	00000097          	auipc	ra,0x0
			32: R_RISCV_CALL	pmkCacheInit
			32: R_RISCV_RELAX	*ABS*
  36:	000080e7          	jalr	ra # 32 <.LVL0>

0000003a <.LVL1>:
  3a:	00000097          	auipc	ra,0x0
			3a: R_RISCV_CALL	pmkCacheRomInit
			3a: R_RISCV_RELAX	*ABS*
  3e:	000080e7          	jalr	ra # 3a <.LVL1>

00000042 <.LBB26>:
  42:	12092583          	lw	a1,288(s2)

00000046 <.LBE26>:
  46:	00000537          	lui	a0,0x0
			46: R_RISCV_HI20	.LC1
			46: R_RISCV_RELAX	*ABS*
  4a:	00048613          	mv	a2,s1
			4a: R_RISCV_LO12_I	.LANCHOR0
			4a: R_RISCV_RELAX	*ABS*
  4e:	0285d5b3          	divu	a1,a1,s0
  52:	00050513          	mv	a0,a0
			52: R_RISCV_LO12_I	.LC1
			52: R_RISCV_RELAX	*ABS*
  56:	00000097          	auipc	ra,0x0
			56: R_RISCV_CALL	dbg_test_print
			56: R_RISCV_RELAX	*ABS*
  5a:	000080e7          	jalr	ra # 56 <.LBE26+0x10>

0000005e <.LVL3>:
  5e:	40b2                	lw	ra,12(sp)
  60:	4422                	lw	s0,8(sp)
  62:	4492                	lw	s1,4(sp)
  64:	4902                	lw	s2,0(sp)
  66:	4501                	li	a0,0
  68:	0141                	addi	sp,sp,16
  6a:	8082                	ret

Disassembly of section .text.supplicantFuncInit:

00000000 <supplicantFuncInit>:
   0:	1141                	addi	sp,sp,-16
   2:	c606                	sw	ra,12(sp)
   4:	c422                	sw	s0,8(sp)
   6:	c226                	sw	s1,4(sp)
   8:	c04a                	sw	s2,0(sp)

0000000a <.LBB34>:
   a:	44b00937          	lui	s2,0x44b00
   e:	12092583          	lw	a1,288(s2) # 44b00120 <.LASF751+0x44afd4a2>

00000012 <.LBE34>:
  12:	3e800413          	li	s0,1000
  16:	000004b7          	lui	s1,0x0
			16: R_RISCV_HI20	.LANCHOR1
			16: R_RISCV_RELAX	*ABS*
  1a:	0285d5b3          	divu	a1,a1,s0
  1e:	00000537          	lui	a0,0x0
			1e: R_RISCV_HI20	.LC0
			1e: R_RISCV_RELAX	*ABS*
  22:	00048613          	mv	a2,s1
			22: R_RISCV_LO12_I	.LANCHOR1
			22: R_RISCV_RELAX	*ABS*
  26:	00050513          	mv	a0,a0
			26: R_RISCV_LO12_I	.LC0
			26: R_RISCV_RELAX	*ABS*
  2a:	00000097          	auipc	ra,0x0
			2a: R_RISCV_CALL	dbg_test_print
			2a: R_RISCV_RELAX	*ABS*
  2e:	000080e7          	jalr	ra # 2a <.LBE34+0x18>

00000032 <.LVL4>:
  32:	00000097          	auipc	ra,0x0
			32: R_RISCV_CALL	supplicantRestoreDefaults
			32: R_RISCV_RELAX	*ABS*
  36:	000080e7          	jalr	ra # 32 <.LVL4>

0000003a <.LBB35>:
  3a:	12092583          	lw	a1,288(s2)

0000003e <.LBE35>:
  3e:	40b2                	lw	ra,12(sp)
  40:	4902                	lw	s2,0(sp)
  42:	0285d5b3          	divu	a1,a1,s0
  46:	4422                	lw	s0,8(sp)
  48:	00048613          	mv	a2,s1
			48: R_RISCV_LO12_I	.LANCHOR1
			48: R_RISCV_RELAX	*ABS*
  4c:	4492                	lw	s1,4(sp)
  4e:	00000537          	lui	a0,0x0
			4e: R_RISCV_HI20	.LC1
			4e: R_RISCV_RELAX	*ABS*
  52:	00050513          	mv	a0,a0
			52: R_RISCV_LO12_I	.LC1
			52: R_RISCV_RELAX	*ABS*
  56:	0141                	addi	sp,sp,16
  58:	00000317          	auipc	t1,0x0
			58: R_RISCV_CALL	dbg_test_print
			58: R_RISCV_RELAX	*ABS*
  5c:	00030067          	jr	t1 # 58 <.LBE35+0x1a>
