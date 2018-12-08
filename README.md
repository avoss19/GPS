# GPS Nav:

Navigation w/ GPS for BSM Robotics

## Run Solo-Machine:

```
python Local.py
```

## Run Multi-Machine:

Run on pi w/ GPS:

```
python Server.py
```

Run on pi w/ drive controller:

```
python Client.py
```

## Setup Solo-Machine:

**Edit `Local.py`:**

Disable PWM:
Uncomment line 5, comment out line 6

Enable PWM:
Comment line 5, uncomment out line 6

Set Goal:
Edit line 8

## Setup Multi-Machine:

**Edit `Client.py`:**

Disable PWM:
Uncomment line 5, comment out line 6

Enable PWM:
Comment line 5, uncomment out line 6

**Edit `Server.py`:**

Set Goal:
Edit line 7
