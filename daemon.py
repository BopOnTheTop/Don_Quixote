import daemon

from don_quixote import main

with daemon.DaemonContext():
    main()