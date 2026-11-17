# Gemini Agent Instructions

## Context

Read README.md to understand the Mini Coding Agent project and how to use it.

For coding tasks, please read the .gemini/tasks/T-###/intent.md, .gemini/tasks/T-###/spec.md, and .gemini/tasks/T-###/plan.md files to understand the task and how to implement it successfully. It should be apparent from those files what the definition of done is for the task. You should ask the user to clarify if the definition of done is not obvious, and then amend the appropriate files. For any questions about this development process structure, please refer to https://claude.com/resources/articles/the-ai-native-sdlc-playbook.

This repo currently implements a mini coding agent with 6 core components outlined in the README.md and explained further at https://magazine.sebastianraschka.com/p/components-of-a-coding-agent.

Finally, .gemini/memory/memory.md should record a log of all planned tasked, completed tasks, questions, and decisions with indexes and updated as changes are made. Also in .gemini/memory are the hooks/ and tools/ directories which should be used to store any hooks, tools, or skills that the user decides to create manually or enlist the agent to create.


## Making contributions

To make contributions, you should become familiar with all necessary context from the repo.

Then, you should suggest a planned implementation of the task to the user and get confirmation to start developing.

Tests should be created in advance using Pytest. Then code should be written to solve the task. Before making a pull request or moving on to another task, you must run all applicable tests using Pytest and ensure coding guidelines are met using ruff.

## Running shell commands

To run a shell command, first see if there are any tools available to do so without needing permission. If no tools exist, describe 1) What the shell command does and 2) Why you would like to call it. If a tool should be created for the shell command, make one at that time or create a note in 