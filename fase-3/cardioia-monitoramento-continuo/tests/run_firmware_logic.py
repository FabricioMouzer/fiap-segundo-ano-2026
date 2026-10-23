"""Testes nativos da lógica extraída do firmware. Não simula ESP32 nem sensores."""
from pathlib import Path
import subprocess
import tempfile

MAIN = 'int main(){\nassert(calculateAlert(36.5,80,true)==0);\nassert(calculateAlert(38.0,50,true)==0);\nassert(calculateAlert(38.0,120,true)==0);\nassert(calculateAlert(36.5,49,true)==1);\nassert(calculateAlert(36.5,121,true)==2);\nassert(calculateAlert(38.1,80,true)==4);\nassert(calculateAlert(0,80,false)==8);\nassert(calculateAlert(39,130,true)==6);\nSampleRingBuffer q;\nassert(q.empty()); q.pop();\nfor(unsigned i=1;i<=721;i++){Sample x{};x.sequence=i;q.push(x);}\nassert(q.size()==720 && q.dropped()==1 && q.front().sequence==2);\nfor(unsigned i=2;i<=721;i++){assert(q.front().sequence==i);q.pop();}\nassert(q.empty());\nputs("PASS: 8 alert scenarios + buffer overflow/FIFO/empty pop (native logic only; not ESP32/Wokwi)");\n}'

ROOT = Path(__file__).resolve().parents[1]
s = (ROOT / "wokwi/sketch.ino").read_text(encoding="utf-8")
code = ("#include <cstdint>\n#include <cstddef>\n#include <cassert>\n#include <cstdio>\nconstexpr uint8_t DHT22=22;\n"
        + s[s.index("namespace Config"):s.index("DHT dht(")]
        + s[s.index("uint8_t calculateAlert("):s.index("Sample collectSample()")]
        + MAIN)
with tempfile.TemporaryDirectory() as directory:
    source = Path(directory) / "logic.cpp"
    binary = Path(directory) / "logic"
    source.write_text(code, encoding="utf-8")
    subprocess.run(["g++", "-std=c++11", "-Wall", "-Wextra", "-pedantic", str(source), "-o", str(binary)], check=True)
    subprocess.run([str(binary)], check=True)
