
from flask import render_template, url_for, redirect
from app import webapp

import datetime


@webapp.route('/')
def main():
    return render_template("main.html")


@webapp.route('/lecture')
def lecture():
    return render_template("lecture/lecture.html")


@webapp.route('/tutorial')
def tutorial():
    return render_template("tutorial/tutorial.html")

