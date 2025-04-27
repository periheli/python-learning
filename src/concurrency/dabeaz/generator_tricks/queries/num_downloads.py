if __name__ == "__main__":
    from apache_log import apache_log
    from gen_file_utils import lines_from_dir

    lines = lines_from_dir("access-log*", "www")
    log = apache_log(lines)

    print(sum(1 for row in log if row["request"] == "/ply/ply-2.3.tar.gz"))
