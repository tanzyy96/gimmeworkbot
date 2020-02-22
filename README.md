# gimmeworkbot

Start date: 7 Feb 2020  
Aim: To build a personal Telegram bot using either the Python or C++ API wrapper  
Target date of completion: 1 Mar 2020

## TODOS

- [x] Try building tutorial bot
- [x] Set up Virtual Environment for project
  - [x] Install packages
  - [x] Troubleshooting
- [ ] Read wiki and implement
  - [x] Basic message and response
  - [x] Saving data
  - [ ] Recalling data
  - [ ] Building tests...?
- [ ] Planning bot design
  - [ ] Bot Function #1 -- Managing ToDos
  - [ ] Bot Function #2
- [ ] Launching bot v1.0
- [ ] Extending bot function
  - [ ] Function #1.1
  - [ ] Function #1.2

## F1: Managing ToDos

The main purpose of this function is to allow me to add todos as quickly as possible. This can also be extendable to other things, such as notes, debts .etc

A few main functions will be required here:

- [ ] General description
  - [ ] /start
  - [ ] /help
- [x] Add todo
  - [x] /todo to add
  - [x] add deadline
  - [x] remove calendar dates before today (or ignore)
- [x] Check todos
  - [x] /list to check
- [ ] Edit todos
  - [ ] Command helper /edit
  - [ ] Enter new todo -> enter new deadline
  - [ ] Confirm callback
- [ ] Delete todo
- [ ] Reminder on deadlines
- [ ] Priorities on todos (we can do color!)
- [ ] Sort todos (we can use context.args on /list here)

## Continue off from here

Next up, we want to allow editing of todos. Might have to implement /edit todo washing, or something like that.

Can actually route it to call existing command helpers for reuse.
