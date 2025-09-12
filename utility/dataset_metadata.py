from datetime import datetime, timezone

def add_standard_metadata(dataset, source_dir, dtype, extra_metadata=None):
    
    now_iso = datetime.now(timezone.utc).isoformat()

    metadata = {
        "created_at": dataset.info.get("created_at", now_iso),
        "modified_at": now_iso,
        "source": source_dir,
        "type": dtype
    }

    if extra_metadata:
        metadata.update(extra_metadata)

    dataset.info.update(metadata)
    dataset.save()