#!/usr/bin/env python3
"""
Amdahl's law illustrator (with fake work to minimize actual CPU load)

Amdahl's law posits that some unit of work comprises a proportion *p* that
benefits from parallel resources, and a proportion *s* that is constrained to
execute in serial, only. The theoretical maximum speedup achievable for such a
workload is

           1
    S = -------
        s + p/N

where *S* is the speedup relative to performing all of the work in serial and
*N* is the number of parallel workers. A plot of *S* vs. *N* ought to look like
this, for *p*=0.8:

  5┬─────────────────────────────────────·──────────────────┐
   │                                   ·                    │
   │                                 ·                      │
   │                               ·                        │
  4┤                             ·                          │
   │                           ·                            │
S  │                         ·                              *
p  │                       ·                   *      *     │
e  │                     ·               *                  │
e 3┤                   ·           *                        │
d  │                 ·      *                               │
u  │               ·  *                                     │
p  │             ·                                          │
   │           ·*                                           |
  2┤         ·                                              │
   │     * ·                                                │
   │     ·                                                  │
   │   ·                                                    │
   │ ·                                                      │
  1*─────┬──────┬─────┬─────┬──────┬─────┬─────┬──────┬─────┤
   1     2      3     4     5      6     7     8      9     10
                             Workers

"Ideal scaling" (*p*=1) would be the line *y* = *x* (or *S* = *N*), represented
by the dotted line.

This graph shows there is a speed limit for every workload, and diminishing
returns on throwing more parallel processors at a problem. It is worth running
a "scaling study" to assess how far away that speed limit might be for the
given task.
"""

import time
# Start a clock to measure total time
start = time.time()

import sys
import argparse

from mpi4py import MPI

def do_work(work_time=30, parallel_proportion=0.8, comm=MPI.COMM_WORLD):
    # How many MPI ranks (cores) are we?
    size = comm.Get_size()
    # Who am I in that set of ranks?
    rank = comm.Get_rank()
    # Where am I running?
    name = MPI.Get_processor_name()

    if rank == 0:
        # Set the sleep times (which are used to fake the amount of work)
        serial_sleep_time = float(work_time) * (1.0 - parallel_proportion)
        parallel_sleep_time = (float(work_time) * parallel_proportion) / size

        # Use Amdahl's law to calculate the expected speedup for this workload
        amdahl_speed_up = 1.0 / (
            (1.0 - parallel_proportion) + parallel_proportion / size
        )

        suffix = "" if size == 1 else "s"

        sys.stdout.write(
            "Doing %f seconds of 'work' on %s processor%s,\n"
            " which should take %f seconds with %f parallel"
            " proportion of the workload.\n\n"
            % (work_time, size, suffix, work_time / amdahl_speed_up, parallel_proportion)
        )

        sys.stdout.write(
            "  Hello, World! I am process %d of %d on %s."
            " I will do all the serial 'work' for"
            " %f seconds.\n" % (rank, size, name, serial_sleep_time)
        )
        time.sleep(serial_sleep_time)
    else:
        parallel_sleep_time = None

    # Tell all processes how much work they need to do using 'bcast' to broadcast
    # (this also creates an implicit barrier, blocking processes until they receive
    # the value)
    parallel_sleep_time = comm.bcast(parallel_sleep_time, root=0)

    # This is where everyone pretends to do work (while really we are just sleeping)
    sys.stdout.write(
        "  Hello, World! I am process %d of %d on %s. I will do parallel 'work' for "
        "%f seconds.\n" % (rank, size, name, parallel_sleep_time)
    )
    time.sleep(parallel_sleep_time)


# Only the root process handles the command line arguments
rank = MPI.COMM_WORLD.Get_rank()
if rank == 0:
    # Initialize our argument parser
    parser = argparse.ArgumentParser(prog="amdahl")

    # Adding optional arguments
    parser.add_argument(
        "-p",
        "--parallel-proportion",
        nargs="?",
        const=0.8,
        type=float,
        default=0.8,
        help="Parallel proportion should be a float between 0 and 1",
    )
    parser.add_argument(
        "-w",
        "--work-seconds",
        nargs="?",
        const=30,
        type=int,
        default=30,
        help="Total seconds of workload, should be an integer greater than 0",
    )

    # Read arguments from command line
    args = parser.parse_args()

    if not args.work_seconds > 0:
        parser.print_help()
        MPI.COMM_WORLD.Abort(1)
        sys.exit(1)

    if args.parallel_proportion <= 0 or args.parallel_proportion > 1:
        parser.print_help()
        MPI.COMM_WORLD.Abort(1)
        sys.exit(1)

    do_work(work_time=args.work_seconds, parallel_proportion=args.parallel_proportion)
    end = time.time()
    sys.stdout.write(
        "\nTotal execution time (according to rank 0): %f seconds\n" % (end - start)
    )
else:
    do_work()
