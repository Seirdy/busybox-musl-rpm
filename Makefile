# Makefile for source rpm: busybox
# $Id$
NAME := busybox
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
