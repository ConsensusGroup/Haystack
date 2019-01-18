#!/bin/bash

PushFrom="a"
PushTo=["b","c","d","e"]

FilesInPushFrom=$PushFrom/*
for i in ${FilesInPushFrom[@]}
do
	for z in ${PushTo[@]}
	do
		if [[ $i == *"Config"* ]] || [[ $i == *"UserData"* ]];
		then
			:
		else
			cp $i $z/
		fi
	done
done

