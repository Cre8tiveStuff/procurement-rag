from    arc import idempotent

@idempotent
def     refresh_index(new_file_path):
        # placeholder:  real ingest/chunk/embed/store calls go here next
        return {"status":  "indexed", "file": str(new_file_path)} 
