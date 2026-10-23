# File: Makefile
# GNU Makefile for the RT Hexadecimal PCIe Interface Driver Subsystem
# Target Environment: Linux Kernel 4.x / 5.x / 6.x

obj-m += hex_pcie_driver.o

# Detect current running kernel tree version path
KDIR ?= /lib/modules/$(shell uname -r)/build
PWD  := $(shell pwd)

default: compile

compile:
	@echo "[Build] Compiling 16-state native PCIe host kernel translation modules..."
	$(MAKE) -C $(KDIR) M=$(PWD) modules

clean:
	@echo "[Build] Clearing compiler workspace artifacts..."
	$(MAKE) -C $(KDIR) M=$(PWD) clean
	rm -f *.o *.ko *.mod *.mod.c .*.cmd modules.order Module.symvers

install: compile
	@echo "[Deploy] Installing kernel object into system module framework trees..."
	install -m 644 hex_pcie_driver.ko /lib/modules/$(shell uname -r)/kernel/drivers/misc/
	depmod -a
	@echo "[Deploy] Verification Complete. Triggering 'modprobe hex_pcie_driver' to activate bus lanes."
