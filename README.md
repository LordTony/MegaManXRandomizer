# MegaManXRandomizer

## Requirements
Get yourself a copy of the "Mega Man X (USA) (Rev 1)" .sfc rom. It can be in a zip folder

## Useage Examples
If you want to randomize your rom with all of the basic settings, it's as simple as this:

```python rando.py "Mega Man X (USA) (Rev 1).sfc"```

also works fine if that file is zipped up:

```python rando.py "Mega Man X (USA) (Rev 1).zip"```

If you want to name the output file, use the `-o` flag:

```python rando.py "Mega Man X (USA) (Rev 1).sfc" -o "My Output File Name.sfc"```

If you want to start with the dash boots so you don't need to do Chill Penguin's stage first, use the `-d` 0r `--dash-boot-start` flag:

```python rando.py "Mega Man X (USA) (Rev 1).sfc" -d ```

If you want the bosses to never drop their original weapons use the `-s` or `--strict-shuffle` flag:

```python rando.py "Mega Man X (USA) (Rev 1).sfc" -s ```

If you want the bosses to never drop their own weakness use the `-n` or `--no-self-weakness` flag:

```python rando.py "Mega Man X (USA) (Rev 1).sfc" -n ```

You can mix and match all of these flags as well like this:

```python rando.py "Mega Man X (USA) (Rev 1).sfc" -dsn ```

## Potential Issues

I haven't even looked at how the passwords work after the game has been randomized. I give it a 50/50 chance that it actually works.