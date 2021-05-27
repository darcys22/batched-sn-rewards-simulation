# Analysis of Service Node batching

Simulates the block outputs before and after batching of SN rewards.

Uses `getcontributors.py` to generate `contributors-dump.json` which has already been generated. But this will call the RPC method on a daemon running at public.loki.foundation to get a list of contributors.

Then `batchsim.py` builds the simulation to output the `batched_savings.png` graph. Optionally viewed in `index.html`

## Running
Uses python3 with pip modules stored in `requirements.txt`

install using 
```
pip3 install -r requirements
```

and run using
```
python3 batchsim.py
```

## Makefile
if you have virtualenv on your path you can call
```
make run
```

which will build a virtualenv specific for this project in the `venv` folder. Will also run using that environment
