# Snake

Ett klassiskt Snake-spel som körs direkt i terminalen. Skrivet i Python med
endast standardbiblioteket (`curses` för rendering/input, `random` för mat) –
inga externa beroenden.

## Kör spelet

```bash
uv run main.py
```

## Spela

- **Piltangenter** – styr ormen
- **`*`** – mat; ät för att växa och få poäng
- Spelet tar slut om ormen krockar med väggen eller sig själv
- **R** – spela igen, **Q** – avsluta

Kräver en interaktiv terminal (curses).
