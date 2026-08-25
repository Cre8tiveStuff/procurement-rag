curl -X POST "http://localhost:8000/query" \
 -H "Content-Type:  application/json" \
 -d '{"query":  "what is the delivery timeline agreed upon by Supplier Inc?", "top_k": 2}'
