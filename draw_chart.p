set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
set format x "%b-%d %H:%M:%S"
set xlabel 'Timestamp'
set ylabel 'Sequence'
plot '/tmp/ledger_info.dat' using 1:3 with linespoints title 'Rippled Ledger'
