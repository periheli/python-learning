if __name__ == "__main__":
    from apache_log import apache_log
    from gen_file_utils import lines_from_dir

    lines = lines_from_dir("access-log*", "www")
    log = apache_log(lines)

    print("%d %s" % max((row["bytes"], row["request"]) for row in log))
