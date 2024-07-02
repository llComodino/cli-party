## CLI Party

- This is a terminal game heavily inspired by the famous [bombparty](https://jklm.fun)

## Installation

- Clone the git repo
```sh
git clone git@github.com:llComodino/cli-party
```

- Install the requirements
```sh
pip3 install -r requirements.txt
```

- Follow the set-up below

- Start the game
```sh
python3 cliparty.py
```

---

## Set-up

Create/download your wordlist, rename it `wordlist.txt`
and place it in the same folder as the script

Create/download your syllable list, rename it `syllables.txt`
and place it in the same folder as the script
> File format:
```text
X;n # where X is your syllable and n an integer (1-5)
```

Create/download your letter set, rename it `letter_set.txt`
and place it in the same folder as the script

> NOTE: All of these files use newline separators
Only `syllables.txt` adds ';' to separate the syllable from the difficulty

---
