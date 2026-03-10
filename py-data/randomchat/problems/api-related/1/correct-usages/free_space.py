from flask import Blueprint, render_template
from randomchat.settings import settings

import socketio
import random
import logging

def free_space(pairs):
	t_list = []
	for i in range(0, len(pairs)):
		if(isinstance(pairs[i], list)):
			if(pairs[i][0] == 'EMPTY' and pairs[i][1] == 'EMPTY'):
				t_list.append(pairs[i])
	for i in range(0, len(t_list)):
		pairs.remove(t_list[i])
