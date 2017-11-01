#!/usr/bin/python

def gen_range_following () :
    s = ""
    for i in range (10) :
        s += str(i*20)+','+str((i+1)*20)+','+str(i*20)+'_'+str((i+1)*20)+' ; '
    print s

def gen_range_days () :
    s = ""
    for i in range (10) :
        s += str(i*1)+','+str((i+1)*1)+','+str(i*1)+'_'+str((i+1)*1)+' ; '
    for i in range (5) :
        s += str(10+i*10)+','+str(10+(i+1)*10)+','+str(10+i*10)+'_'+str(10+(i+1)*10)+' ; '
    print s

# gen_range_following ()
gen_range_days()
