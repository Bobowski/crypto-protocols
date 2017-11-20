# Schnorr Identification Protocol

## General informations:

- Using **charm-crypto** python3 library (python2 should be compatible)
- Using **SS512** pairing-curve whenever possible (idk yet why, but it works)
- Json style format for exchange messages (parameters depend on scheme)
- Json messages are exchanged via any medium necessary (FB, e-mail, birds, bottles etc.)

## How-To:
1. Generate keypair. If using random *g* just hit return, else paste base64 encoded g value (from charm-crypto). It outputs `cred.pk` and `cred.sk` json files with keys.
  ```
  ./keygen.py
  ```
2. Run `prover.py` and `verifier.py` in separate terminal windows to test if protocol works. All you have to do is paste whole json messages that are writted by one terminal into the second one

## Exchange format:
```
TODO
```

## Special thanks:
1. *Dr Krzywiecki* - for awesome tasks to complete
2. *Me* - for great patience with completing those exercises


