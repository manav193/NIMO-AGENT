"""Minimal memory context injection; raw vault records never go directly to the model."""
class MemoryContext:
    def build(self,hits,max_chars=6000):
        out=[]; total=0
        for h in hits:
            text=f"[memory:{h.record_id}] {h.text}"
            if total+len(text)>max_chars: break
            out.append(text); total+=len(text)
        return "\n".join(out)
