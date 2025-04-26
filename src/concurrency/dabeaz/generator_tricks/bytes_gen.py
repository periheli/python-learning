from gen_file_utils import gen_cat, gen_find, gen_grep, gen_open

pattern = r"ply-.*\.gz"
log_dir = "www"

file_names = gen_find("access-log*", log_dir)
log_files = gen_open(file_names)
log_lines = gen_cat(log_files)
matched_lines = gen_grep(pattern, log_lines)
byte_column = (line.rsplit(None, 1)[1] for line in matched_lines)
bytes_sent = (int(x) for x in byte_column if x != "-")

print("Total", sum(bytes_sent))
