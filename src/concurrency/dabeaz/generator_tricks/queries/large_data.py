if __name__ == "__main__":
    from apache_log import apache_log
    from gen_file_utils import lines_from_dir

    lines = lines_from_dir("access-log*", "www")
    log = apache_log(lines)

    large_rows = (row for row in log if row["bytes"] > 1_000_000)

    for row in large_rows:
        print(row["request"], row["bytes"])
