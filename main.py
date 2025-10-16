#!/usr/bin/env python3
"""
Example realistic main for JSON generator (non-destructive).
"""
import random, json, argparse, string, sys

def rand_string(length=8):
    choices = string.ascii_letters + string.digits
    return ''.join(random.choice(choices) for _ in range(length))

def rand_number(minv=0, maxv=100):
    return random.randint(minv, maxv)

def gen_field(spec):
    t = spec.get("type", "string")
    if t == "string":
        return rand_string(spec.get("length", 8))
    if t == "int":
        return rand_number(spec.get("min", 0), spec.get("max", 100))
    if t == "list":
        cnt = spec.get("count", 3)
        item = spec.get("item", {"type": "string", "length": 6})
        return [gen_field(item) for _ in range(cnt)]
    if t == "bool":
        return random.choice([True, False])
    return None

def sample_schema():
    return {
        "id": {"type": "string", "length": 12},
        "age": {"type": "int", "min": 18, "max": 80},
        "tags": {"type": "list", "count": 4, "item": {"type": "string", "length": 6}},
        "active": {"type": "bool"},
        "score": {"type": "int", "min": 0, "max": 1000}
    }

def generate(schema, count=1, seed=None):
    if seed is not None:
        random.seed(seed)
    out = []
    for _ in range(count):
        obj = {}
        for k, v in schema.items():
            obj[k] = gen_field(v)
        out.append(obj)
    return out

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--count", "-n", type=int, default=3)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--schema", "-s", help="schema json file")
    p.add_argument("--pretty", action="store_true")
    args = p.parse_args()
    schema = sample_schema()
    if args.schema:
        try:
            with open(args.schema, 'r', encoding='utf-8') as fh:
                schema = json.load(fh)
        except Exception:
            pass
    res = generate(schema, count=args.count, seed=args.seed)
    if args.pretty:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(res, ensure_ascii=False))

if __name__ == "__main__":
    sys.exit(main())
