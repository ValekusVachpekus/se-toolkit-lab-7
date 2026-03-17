# Autochecker

<h2>Table of contents</h2>

- [What is the `Autochecker`](#what-is-the-autochecker)
- [The `Autochecker` bot](#the-autochecker-bot)
- [The `Autochecker` agent](#the-autochecker-agent)
- [Set up the `Autochecker`](#set-up-the-autochecker)
  - [Open the `Autochecker` bot](#open-the-autochecker-bot)
  - [Log in to the `Autochecker` bot](#log-in-to-the-autochecker-bot)
  - [Add the `SSH` public key for the `Autochecker` agent (REMOTE)](#add-the-ssh-public-key-for-the-autochecker-agent-remote)
- [Check the task using the `Autochecker` bot](#check-the-task-using-the-autochecker-bot)

<!-- TODO review -->

## What is the `Autochecker`

The autochecker is a system that you can ask to [check](#check-the-task-using-the-autochecker-bot) your repository and your VM when you work on a task.

It has two main components:

- [The `Autochecker` bot](#the-autochecker-bot)
- [The `Autochecker` agent](#the-autochecker-agent)

## The `Autochecker` bot

The `Autochecker` bot in Telegram.

<https://t.me/auchebot>

## The `Autochecker` agent

An agent that can check [your VM](./vm.md#your-vm) setup.

## Set up the `Autochecker`

Complete these steps:

<!-- no toc -->
1. [Open the `Autochecker` bot](#open-the-autochecker-bot).
2. [Log in to the `Autochecker` bot](#log-in-to-the-autochecker-bot).
3. [Add the `SSH` public key for the `Autochecker` agent (REMOTE)](#add-the-ssh-public-key-for-the-autochecker-agent-remote).

### Open the `Autochecker` bot

Open in `Telegram`: <https://t.me/auchebot>.

### Log in to the `Autochecker` bot

1. [Open the `Autochecker` bot](#open-the-autochecker-bot)
2. Log in.

### Add the `SSH` public key for the `Autochecker` agent (REMOTE)

> [!NOTE]
> Replace [`<user>`](./operating-system.md#user-placeholder) with the actual [username](./operating-system.md#username).
>
> Add the [`SSH` public key](./ssh.md#ssh-public-key) for [the `Autochecker` agent](#the-autochecker-agent) so that it can access your VM as the user `<user>`.

1. [Connect to your VM as the user `<user>`](./vm-access.md#connect-to-your-vm-by-ssh-as-the-user-user-local).

2. To check whether the `SSH` public key is already present,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   grep se-toolkit-autochecker ~/.ssh/authorized_keys
   ```

   Skip the following steps in this section if you see:

   ```terminal
   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKiL0DDQZw7L0Uf1c9cNlREY7IS6ZkIbGVWNsClqGNCZ se-toolkit-autochecker
   ```

3. To add the `SSH` public key,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKiL0DDQZw7L0Uf1c9cNlREY7IS6ZkIbGVWNsClqGNCZ se-toolkit-autochecker" >> ~/.ssh/authorized_keys
   ```

4. To verify the `SSH` public key was added,

   [run in the `VS Code Terminal`](./vs-code.md#run-a-command-in-the-vs-code-terminal):

   ```terminal
   grep se-toolkit-autochecker ~/.ssh/authorized_keys
   ```

   You should see:

   ```terminal
   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKiL0DDQZw7L0Uf1c9cNlREY7IS6ZkIbGVWNsClqGNCZ se-toolkit-autochecker
   ```

## Check the task using the `Autochecker` bot

1. [Open the `Autochecker` bot](#open-the-autochecker-bot)
2. Click the lab.
3. Click the task.
