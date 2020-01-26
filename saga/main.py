#!/usr/bin/env python3
from saga.commands.parser import create_saga_parser


def main():
    parser = create_saga_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
