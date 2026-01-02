# Fáze 3 Control Flow Refactoring - Pokračování

## 🎯 AKTUÁLNÍ STAV (2026-01-01)

### ✅ CO JE HOTOVÉ

#### Fáze 1 & 2 (KOMPLETNÍ)
- **Fáze 1A**: Switch bloky se označují jako emitted → eliminuje unreachable bloky
- **Fáze 1B**: Skip goto na switch header → eliminuje `goto block_X` PŘED switchy
- **Fáze 2A**: Odstraněna if/else pre-detection
- **Fáze 2B**: Runtime if/else detection během renderingu
- **Fáze 2C**: Podpora if-without-else (1 successor)

**Výsledek**: 100% eliminace goto před switchy, 0 chyb, verified na 4 souborech

#### Fáze 3A: Loop Detection & Conversion (KOMPLETNÍ) ✅
- **Implementována `_render_blocks_with_loops()`**: Renderuje bloky s loop detection supportem
- **Implementována `_detect_for_loop()`**: Detekuje for-loop pattern (init, condition, increment)
- **Upraveno switch case rendering**: Používá `_render_blocks_with_loops()` pro case bodies
- **Přidán `ForLoopInfo` dataclass**: Ukládá informace o for-loop structure

**Výsledek**: 100% for-loop detection v tdm.scr (3/3 loops), loops renderují jako `for(i=0; i<N; i++)`

**Dokumentace**: `docs/for_loop_detection_implementation.md`

**Soubory**:
- `vcdecomp/core/ir/structure.py` - obsahuje všechny Fáze 1 & 2 fixy
- `control_flow_refactoring.md` - kompletní dokumentace

---

## 📋 CO ZBÝVÁ IMPLEMENTOVAT

### ~~Fáze 3A: Loop Detection & Conversion~~ ✅ HOTOVO

**Status**: ✅ **DOKONČENO 2026-01-01** - Přesunuto do "CO JE HOTOVÉ" sekce výše.

---

### Fáze 3A (PŮVODNÍ POPIS - ARCHIVOVÁNO)

**Problém**: For-loops se vůbec nerenderují
```c
// CURRENT:
local_2 = 0;
// Block 27
(0 + (i * 4)) = value;
local_2 = (i + 1);

// SHOULD BE:
for (i = 0; i < gRecs; i++)
    gRecTimer[i] -= info->elapsed_time;
```

**Implementace**:

1. **Nová funkce `_detect_for_loop`** (~50 řádků)
   ```python
   def _detect_for_loop(loop: NaturalLoop, cfg: CFG, ssa_func: SSAFunction) -> Optional[ForLoopInfo]:
       """
       Detect for-loop pattern:
       1. Find initialization block (predecessor of header)
          - Look for pattern: i = 0, local_X = 0
       2. Extract condition from header's conditional jump
          - Parse: i < N, local_X < gRecs, etc.
       3. Find increment at end of loop body
          - Look for: i++, i+=1, local_X = (i + 1)
       4. Return ForLoopInfo(var, init, cond, incr) or None
       """
   ```

   **ForLoopInfo dataclass**:
   ```python
   @dataclass
   class ForLoopInfo:
       var: str           # Loop variable (e.g., "i", "local_2")
       init: str          # Initialization (e.g., "0")
       condition: str     # Loop condition (e.g., "i < gRecs")
       increment: str     # Increment expr (e.g., "i++")
   ```

2. **Upravit loop rendering** (structure.py řádky ~862-883)
   ```python
   # CURRENT:
   lines.append(f"{indent}while (true) {{")

   # NEW:
   for_info = _detect_for_loop(header_loop, cfg, ssa_func)
   if for_info:
       lines.append(f"{indent}for ({for_info.var} = {for_info.init}; {for_info.condition}; {for_info.increment}) {{")
   else:
       lines.append(f"{indent}while (true) {{")
   ```

**Test files**: tdm.scr (řádky 63-67 → should be for-loop), Gaz_67.scr (6 loops)

**Priorita**: **HIGHEST** (very high frequency, high impact)

---

### Fáze 3B: Recursive Structure Detection

**Problém 1**: If/else uvnitř switch cases
```c
// CURRENT (tdm.scr lines 18-40):
case 0:
    // Block 3
    // Block 5
    SC_MP_EndRule_SetTimeLeft(...);
    // Block 6
    SC_LoadNextMap();

// SHOULD BE:
case 0:
    if (gPlayersConnected > 0) gTime += time;
    SC_EndRule_SetTimeLeft(...);
    if (gTime > gEndValue) {
        SC_LoadNextMap();
        return TRUE;
    }
    break;
```

**Implementace**:

1. **Upravit `_format_block_lines` signature** (structure.py řádky 75-172)
   ```python
   def _format_block_lines(
       ssa_func: SSAFunction,
       block_id: int,
       indent: str,
       formatter: ExpressionFormatter,
       # NEW PARAMS for recursive detection:
       block_to_if: Optional[Dict[int, IfElsePattern]] = None,
       visited_ifs: Optional[Set[int]] = None,
       cfg: Optional[CFG] = None,
       start_to_block: Optional[Dict[int, int]] = None,
       resolver: Optional[opcodes.OpcodeResolver] = None
   ) -> List[str]:
   ```

2. **Add recursive check BEFORE rendering statements**:
   ```python
   # At start of _format_block_lines:
   if block_to_if and block_id in block_to_if and block_id == block_to_if[block_id].header_block:
       # This block is an if/else header - render as structure
       return _render_if_else_recursive(
           block_to_if[block_id], indent, ssa_func, formatter,
           block_to_if, visited_ifs, cfg, start_to_block, resolver
       )

   # Existing logic for normal blocks...
   ```

3. **Nova funkce `_render_if_else_recursive`** (~80 řádků)
   ```python
   def _render_if_else_recursive(
       if_pattern: IfElsePattern,
       indent: str,
       ssa_func: SSAFunction,
       formatter: ExpressionFormatter,
       block_to_if: Dict[int, IfElsePattern],
       visited_ifs: Set[int],
       cfg: CFG,
       start_to_block: Dict[int, int],
       resolver: opcodes.OpcodeResolver
   ) -> List[str]:
       """
       Recursively render if/else with nested structures.

       1. Get condition from SSA
       2. Render: if (condition) {
       3. For each block in true_body:
          - Call _format_block_lines (will recurse if nested if/else)
       4. If false_body exists:
          - Render: } else {
          - For each block in false_body:
            - Call _format_block_lines (recursive)
       5. Render: }
       6. Mark visited_ifs to prevent re-rendering
       """
   ```

4. **Update all call sites** to pass new params:
   - Switch case rendering (řádky ~750, ~789)
   - Loop body rendering
   - Top-level block rendering

**Test files**: tdm.scr (nested if in switch), hitable.scr

**Priorita**: **HIGH** (medium-high frequency, high impact)

---

### Fáze 3C: Cleanup

#### 1. Odstranit prázdné block comments

**Problém**: Clutter v outputu
```c
// Block 43 @466
// Block 44 @470    ← EMPTY!
SC_MP_GetSRVsettings(&local_74);
```

**Implementace**:

1. **Nova helper funkce**:
   ```python
   def _is_control_flow_only(ssa_inst: SSAInstruction) -> bool:
       """Check if instruction is only control flow (no visible statements)."""
       return resolver.is_jump(ssa_inst.opcode) or resolver.is_return(ssa_inst.opcode)
   ```

2. **Upravit v `_format_block_lines`** (~řádek 110):
   ```python
   # BEFORE:
   lines.append(f"{indent}// Block {block_id} @{block.start}")

   # AFTER:
   # Only add comment if block has actual statements
   has_statements = any(
       not _is_control_flow_only(inst)
       for inst in ssa_block
   )
   if has_statements:
       lines.append(f"{indent}// Block {block_id} @{block.start}")
   ```

**Priorita**: **MEDIUM** (high frequency, low impact, LOW complexity)

---

#### 2. Opravit goto po switchi (dokončit Phase 1A)

**Problém**: hitable.scr má `goto block_6` po switch end

**Implementace** (structure.py po řádku 799):
```python
# After switch closing brace
lines.append(f"{base_indent}}")
emitted_switches.add(block_id)
emitted_blocks.update(switch.all_blocks)
if switch.exit_block is not None:
    emitted_blocks.add(switch.exit_block)

# NEW: Skip next block if it's unreachable connector
if idx + 1 < len(func_blocks):
    next_addr, next_block_id, next_block = func_blocks[idx + 1]
    next_block_obj = cfg.blocks.get(next_block_id)

    # If next block is just a connector (no statements, just jump)
    if next_block_obj and len(next_block_obj.instructions) <= 1:
        # Check if it's jumping to already-emitted block
        if next_block_obj.instructions:
            last = next_block_obj.instructions[-1]
            if resolver.is_jump(last.opcode):
                target = start_to_block.get(last.arg1, -1)
                if target in emitted_blocks:
                    # Skip this connector block
                    emitted_blocks.add(next_block_id)
```

**Priorita**: **MEDIUM** (low frequency, medium impact, LOW complexity)

---

## 🚀 IMPLEMENTAČNÍ PLÁN

### Doporučené pořadí:

1. **START: Fáze 3C** (30 min) - quick wins pro čistší output
   - Implementovat _is_control_flow_only
   - Cleanup empty block comments
   - Fix goto after switch

2. **Fáze 3A** (60-90 min) - highest impact
   - Implementovat ForLoopInfo dataclass
   - Implementovat _detect_for_loop
   - Update loop rendering
   - TEST na tdm.scr, Gaz_67.scr

3. **Fáze 3B** (90-120 min) - complex but critical
   - Update _format_block_lines signature
   - Implementovat _render_if_else_recursive
   - Update all call sites
   - TEST na tdm.scr nested structures

---

## ⚠️ RIZIKA & MITIGACE

### Riziko 1: Loop detection může selhat
**Mitigace**: Fallback na `while(true)` když pattern není rozpoznán

### Riziko 2: Recursive detection → infinite loop
**Mitigace**:
- Strict `visited_ifs` tracking
- Max recursion depth limit (např. 10)
- Assert checks před rekurzí

### Riziko 3: Cleanup odstraní užitečné comments
**Mitigace**: Conservative approach - odstranit JEN bloky s 0 statements

---

## 🧪 TESTOVÁNÍ

### Po každé fázi spustit:
```bash
python -m vcdecomp structure "Compiler-testruns/Testrun1/tdm.scr"
python -m vcdecomp structure "Compiler-testruns/Testrun3/hitable.scr"
python -m vcdecomp structure "Compiler-testruns/Testrun2/Gaz_67.scr"
```

### Success Criteria:
- ✅ **Fáze 3A**: For-loops renderují jako `for(i=0; i<N; i++)`
- ✅ **Fáze 3B**: If/else uvnitř switch cases správně vnořené
- ✅ **Fáze 3C**: < 20% prázdných block comments, 0 goto po switchi
- ✅ **Overall**: 0 Python errors, 0 regressions

---

## 📁 SOUBORY

### K Modifikaci:
- `vcdecomp/core/ir/structure.py` (jediný soubor!)
  - Přidat ForLoopInfo dataclass (top of file)
  - Přidat _detect_for_loop (~50 řádků)
  - Přidat _render_if_else_recursive (~80 řádků)
  - Přidat _is_control_flow_only (~5 řádků)
  - Upravit _format_block_lines signature
  - Upravit loop rendering (řádky 862-883)
  - Upravit empty block comment logic
  - Upravit goto-after-switch logic

**Net change**: ~+135 řádků nového kódu

### K Vytvoření:
- `control_flow_refactoring_phase3.md` - dokumentace Phase 3

---

## 📚 REFERENCE

### Existující Code Patterns:

#### Jak se aktuálně renderují loops (structure.py:862-883):
```python
if header_loop:
    emitted_loop_headers.add(block_id)
    active_loops.append(header_loop)
    indent = "    " + "    " * (len(active_loops) - 1)
    lines.append(f"{indent}// Loop header - Block {block_id} @{addr}")
    lines.append(f"{indent}while (true) {{  // loop body: blocks {sorted(header_loop.body)}")
```

#### Jak se aktuálně renderuje if/else (structure.py:800-863):
```python
if block_id in block_to_if and block_id == block_to_if[block_id].header_block:
    if_pattern = block_to_if[block_id]
    # Get condition...
    lines.append(f"{base_indent}if ({cond_text}) {{")
    # Render true body...
    if if_pattern.false_body:
        lines.append(f"{base_indent}}} else {{")
        # Render false body...
    lines.append(f"{base_indent}}}")
```

#### Jak se volá _format_block_lines (structure.py:750, 789):
```python
# In switch case rendering:
lines.extend(_format_block_lines(ssa_func, body_block_id, base_indent + "    ", formatter))

# In if/else rendering:
lines.extend(_format_block_lines(ssa_func, true_block_id, base_indent + "    ", formatter))
```

**POZOR**: Všechna volání _format_block_lines musí být updated s novými params!

---

## 🎓 KLÍČOVÉ KONCEPTY

### NaturalLoop (cfg.py):
```python
@dataclass
class NaturalLoop:
    header: int              # Loop header block ID
    body: Set[int]          # All blocks in loop body
    exits: Set[int]         # Exit blocks
    back_edges: List[Tuple[int, int]]  # Edges going back to header
```

### IfElsePattern (structure.py:20-33):
```python
@dataclass
class IfElsePattern:
    header_block: int        # Block with conditional jump
    true_block: int          # First block of true branch
    false_block: Optional[int]  # First block of false branch (None for if-without-else)
    merge_block: Optional[int]  # Where branches converge
    true_body: Set[int]      # All blocks in true branch
    false_body: Set[int]     # All blocks in false branch
```

### SSA Values:
- `SSAValue.alias` - může být "local_2", "i", "data_322"
- `SSAValue.name` - fallback když alias není dostupný
- `formatter.render_value(value)` - vrací string representation

---

## 💡 TIPS

### For-Loop Detection:
1. Header má conditional jump (JZ/JNZ)
2. Predecessor of header má assignment (i = 0)
3. Last block in body má increment (i = i + 1)
4. Condition testuje loop variable (i < N)

### Recursive Detection:
1. VŽDY check `visited_ifs` před rekurzí
2. Pass všechny context params down
3. Return early pokud block už byl visited

### Empty Block Detection:
1. Block s JEN jump instrukcí = empty
2. Block s JEN assignments před jump = NOT empty
3. Conservative approach - když nejsi jistý, nech comment

---

## 🔍 DEBUG TIPS

### Když loop detection nefunguje:
1. Print loop header block ID
2. Print predecessor blocks
3. Print last instruction in body blocks
4. Check if increment pattern matches

### Když recursive detection spadne:
1. Add max depth counter (fail after 10 levels)
2. Print recursion path (block_id chain)
3. Check `visited_ifs` state

### Když se objeví duplicitní bloky:
1. Check `emitted_blocks` tracking
2. Verify recursive calls mark blocks as emitted
3. Look for missing `continue` after rendering

---

## ✅ CHECKLIST PRO NOVOU SESSION

1. [ ] Přečíst tento soubor kompletně
2. [ ] Načíst `control_flow_refactoring.md` (Fáze 1 & 2 context)
3. [ ] Otevřít `vcdecomp/core/ir/structure.py`
4. [ ] Začít s **Fáze 3C** (quick wins)
5. [ ] Pak **Fáze 3A** (loop detection)
6. [ ] Nakonec **Fáze 3B** (recursive structures)
7. [ ] Testovat po každé fázi
8. [ ] Vytvořit dokumentaci Phase 3
9. [ ] Final test na všech souborech

---

**Last Updated**: 2026-01-01
**Session Tokens Used**: 118K / 200K
**Status**: Ready for Phase 3 implementation
**Next Step**: Start new session, begin with Phase 3C cleanup
