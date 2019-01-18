#! /usr/bin/python
"""
#+
# NAME:
#    burndisk
# PURPOSE:
#    Burn CD or DVD from directory tree
# CALLING SEQUENCE:
#    burndisk.py [-tar] directory
# INPUTS:
#    directory    top of directory tree to be burned on CD
# OPTIONAL INPUTS:
#    -tar        create zipped tar file and burn CD/DVD
#    -dvd        needed to burn DVDs
#    -img        only creates the CD image (no burning)
#            (in this case -nosudo and -dvd are ignored)
#    -nosudo        launch cdrecord without using sudo
#            By default cdrecord is called using sudo.
#            This requires that /etc/sudoers is set up
#            correctly (see RESTRICTIONS).
#            If -nosudo is set then cdrecord is called directly.
#            This requires special user privileges. Never seem
#            to get it to work right.
#     -verbose    produces more informational messages
#    -temp=temp    directory where the CD image file and
#            tar file are created (default: $TUB)
#    -count=count    indicates number of copies to be burned
#            (default:1)
#    -speed=speed    write speed; default: none
#    -mode=mode    burn mode; default: sao.
#            See REMARKS.
#    -dev=dev    scsi dev for writer. Default: none
#    -email=email    comma-separated list of email addresses to which
#            to send an email upon completion.
#    -exe=exe    name of executable to use for burning disk
#    -nojoliet    omits -J on mkisofs
#    -links        adds -f to mkisofs (follows soft links)
#
#    Some of keywords can be stored in env vars (a command line keyword always
#    takes precedence though):
#
#    If make_dvd SET (burning DVDs):
#        keyword -mode:    DVDMODE        write mode
#        keyword -speed    DVDSPEED    write speed
#    If make_dvd NOT set (burning CDs)
#        keyword -mode:    CDMODE        write mode
#        keyword -dev:    CDSPEED        write speed
#
# RESTRICTIONS:
#    Burning the CD requires the program mkisofs to create the ISO file.
#    The CD/DVD is burned using cdrecord, or wodim (should be available
#    since Fedore Core 7).
#
# REMARKS:
#    I think, sao (session at once) is the same as dao (disk at once).
#    This is the default for cdrecord on most (but not all) of our Linux boxes.
#    Some versions use tao (track at once) by default.
#    One version of cdrecord we use does not accept mode sao at all, but when
#    called with dao said it was running in sao mode. Go figure.
#
#    
# RESTRICTIONS:
#    By default sudo is used to execute cdrecord. This requires that
#    /etc/sudoers needs to be set up correctly. Add a line like:
#        username   ALL=(ALL) NOPASSWD: <dir1>/cdrecord,<dir2>/cdrecord-ProDVD
#    (remember to 'chmod u-w /etc/sudoers' after modifying the file or sudo
#    will refuse to access it).
#
# PROCEDURE:
#    The CD image and the tarball (if -tar is set) are created
#    in 'tempdir', and are deleted after processing.
#
#    If called from another Python module:
#        status = burndisk(alldirs, burn_args)
#    then 'alldirs' is a list of directories, and burn_args is a
#    dictionary, set up with:
#    burn_args = dict    \
#        ( [                \
#          ( 'make_tar', is_there( '-tar'   , sys.argv ) ),    \
#          ( 'make_dvd', is_there( '-dvd'   , sys.argv ) ),    \
#          ( 'make_img', is_there( '-img'   , sys.argv ) ),    \
#          ( 'nosudo'  , is_there( '-nosudo', sys.argv ) ),    \
#          ( 'verbose' , is_there( '-verbose',sys.argv ) ),    \
#          ( 'tempdir' , start   ( '-temp=' , sys.argv ) ),    \
#          ( 'count'   , start   ( '-count=', sys.argv ) ),    \
#          ( 'speed'   , start   ( '-speed=', sys.argv ) ),    \
#          ( 'dev'     , start   ( '-dev='  , sys.argv ) ),    \
#          ( 'email'   , start   ( '-email=', sys.argv ) ),    \
#          ( 'exe'     , start   ( '-exe='  , sys.argv ) ),    \
#          ( 'nojoliet', is_there( '-nojoliet',sys.argv) ),    \
#          ( 'links'   , is_there( '-links=', sys.argv ) )    ] )
# MODIFICATION HISTORY:
#    MAR-2003, Paul Hick (UCSD/CASS)
#    JUL-2003, Paul Hick (UCSD/CASS)
#        Modified to allow for multiple directories on cmd line.
#    OCT-2003, Paul Hick (UCSD/CASS)
#        Fixed bug with -tar keyword
#    JAN-2004, Paul Hick (UCSD/CASS)
#        Merged Austin Duncans burn_a_dvd.py with burn_a_cd.py and
#        renamed it burndisk.py. To burn DVDs set keyword -dvd
#    FEB-2004, Paul Hick (UCSD/CASS)
#        Modified to make callable from other Python modules
#        Added -temp keyword to set directory where tar ball and
#        CD image are created.
#        Added -count keyword to set # copies to be burned
#    MAR-2004, Paul Hick (UCSD/CASS)
#        Added -speed, -verbose and -dev keywords.
#        Changed to dictionary for list of args
#        Added a return value to burndisk. Status=0 is supposed
#        to indicate a succesful creation of a CD/DVD. ... Right.
#        For multiple directories the -graft-points option on mkisofs is
#        now used. The name of the subdirectory is used as the graft point.
#    JUL-2004, Paul Hick (UCSD/CASS)
#        Added check for env vars CDSPEED, CDWR, CDMODE (-dvd not set)
#        or DVDSPEED, DVDWR, DVDMODE (-dvd set) after checking for command
#        line arguments.
#    AUG-2004, Paul Hick (UCSD/CASS)
#        Replaced -sudo by -nosudo. Set default mode to sao.
#        Modified selection of program to burn CD/DVD.
#    AUG-2004, Paul Hick (UCSD/CASS; pphick@ucsd.edu)
#        Added -exe, -nojoliet and -links keyword
#    OCT-2005, Paul Hick (UCSD/CASS)
#        Modified selection of CD/DVD burning program. The default now
#        is cdrecord (which comes with the Linux distribution, usually
#        in /usr/bin). If this is not found then cdrecord-ProDVD is used,
#        if available. Remember that for burning DVDs this last program
#        requires cdrecord-wrapper.sh and a valid license key.
#    NOV-2005, Paul Hick (UCSD/CASS)
#        Added -dev=auto option to detect device name of CD/DVD device.
#        Currently this will select the first device returned by
#        cdrecord -scanbus (so it may not have the desired effect if
#        more than one CD/DVD device is present).
#    DEC-2007, Paul Hick (UCSD/CASS; pphick@ucsd.edu)
#        Removed references to cdrecord-ProDVD. Now the scripts first
#        looks for wodim (available since FC7) or cdrecord.
#        Env vars CDWR and DVDWR are not used anymore. To add the 'dev'
#        switch the -dev keyword must now be explicitly set.
#-
"""
import os,sys
import tiny
from tiny import start, is_there, dict_entry, run_cmd, tomb, hide_env, args

def burndisk(alldirs, burn_args):

    say = 'burndisk, '

    tempdir  = dict_entry( burn_args, 'tempdir' , os.environ['TUB'] )
    make_tar = dict_entry( burn_args, 'make_tar', 0 )
    make_dvd = dict_entry( burn_args, 'make_dvd', 0 )
    make_img = dict_entry( burn_args, 'make_img', 0 )
    nosudo   = dict_entry( burn_args, 'nosudo'  , 0 )
    verbose  = dict_entry( burn_args, 'verbose' , 0 )
    links    = dict_entry( burn_args, 'links'   , 0 )
    nojoliet = dict_entry( burn_args, 'nojoliet', 0 )

    speed = dict_entry( burn_args, 'speed', '' )
    dev   = dict_entry( burn_args, 'dev'  , '' )
    mode  = dict_entry( burn_args, 'mode' , '' )
    email = dict_entry( burn_args, 'email', '' )
    exe   = dict_entry( burn_args, 'exe'  , '' )
    count = dict_entry( burn_args, 'count','1' )
    count = int( count )

    disk = (['CD','DVD'])[make_dvd]

    if dev == 'auto':

        burncmd = run_cmd( 'which wodim 2> /dev/null', 0 )
        if burncmd == '':
            burncmd = run_cmd( 'which cdrecord 2> /dev/null', 0 )

        if burncmd == '':
            status = 1
            print (say+'unable to find wodim or cdrecord')
            return status

        burncmd = (burncmd.split( '\n' ))[0]
        dev = ''
        for tmp in (run_cmd(burncmd+' -scanbus 2> /dev/null', 0)).split('\n'):
            if tmp[0:1] == '\t':
                blank,dev,name = tmp.split('\t')
                if '*' not in name:
                    break

        if dev == '':
            status = 1
            print (say+'unable to determine '+disk+' writer')
            return status

        print (say+'with '+dev+' = '+name)

    if speed == '': speed = dict_entry( os.environ, disk+'SPEED', ''      )
    if mode  == '': mode  = dict_entry( os.environ, disk+'MODE' , 'sao'   )

    if mode != '': mode = '-'+mode
    graft = ''
    is_image = 0

    if make_tar:

        top_dir = ' '.join( alldirs )

        # Create a tarball

        archive = os.path.join(tempdir,'burndisk.tar.gz')
        run_cmd( 'tar -czvf '+archive+' '+top_dir, verbose )

        size = '%d'%(os.stat(archive)).st_size
        print (archive, size, 'bytes (', tomb( size ), 'MB)\n')

    elif len( alldirs ) == 1:

        # If a single file is specified, assume it is a CD/DVD image

        archive = alldirs[0]
        is_image = os.path.isfile( archive )

    else:
        graft = '-graft-points'
        archive = ''

        for subdir in alldirs:
            if subdir[len(subdir)-1] == '/':
                tmp = subdir[0:len(subdir)-1]
            else:
                tmp = subdir

            archive += ' '+(os.path.split(tmp))[1]+'/='+tmp

        archive = archive[1:len(archive)]

    if is_image:

        make_img = 0
        cd_img = archive

    else:
        # Create the CD image from the tar archive (make_tar = 1)
        # or from the top directory (make_tar = 0).

        cd_img  = os.path.join(tempdir,'burndisk.img')
        print (say+'mkisofs ...')

        options = ' -R'
        if not nojoliet: options += 'J'
        if links: options += ' -f'

        run_cmd( 'mkisofs '+graft+options+' -quiet -o '+cd_img+' '+archive, verbose )

    if make_tar:
        os.remove( archive )

    # Are we burning a CD or a DVD

    if not os.path.exists(cd_img):

        # There should be a disk image file available

        status = 1
        message = disk+' image does not exist: '+hide_env(cd_img)

    elif make_img:

        # Disk image has been made. Skip burning of CD/DVD

        status = 0
        message = disk+' image is '+hide_env(cd_img)

    else:

        # Burn CD/DVD

        cd_size = '%d'%(os.stat(cd_img)).st_size
        status = 0

        if exe == '':

            # Keyword -exe NOT set. Select burn executable here.
            # The first choice is wodim. The second is cdrecord.

            burncmd = run_cmd( 'which wodim 2> /dev/null', 0 )
            if burncmd == '':
                burncmd = run_cmd( 'which cdrecord 2> /dev/null', 0 )

            if burncmd == '':
                message = 'unable to find wodim or cdrecord'
                status = 1

        else:

            # Keyword -exe SET. Find the executable

            print (say+exe+' ...')
            burncmd = run_cmd( 'which '+exe, 0 )

            if burncmd == '':
                message = 'unable to find '+exe
                status = 1

        burncmd = (burncmd.split( '\n' ))[0]

        # Write the CD, then remove the CD image file

        if status == 0:

            cmd = (['sudo',burncmd])[nosudo]

            args = []
            if not nosudo: args.append( 'sudo' )
            args.extend( [burncmd, '-eject', '-data'] )
            if dev   != '': args.append( 'dev='  +dev   )
            if speed != '': args.append( 'speed='+speed )
            if mode  != '': args.append( mode )
            args.append( cd_img )

            # If run_cmd can be made to return a proper error code it would
            # probably be a better way to execute cdrecord
            #run_cmd( burncmd, verbose )

            status = os.spawnvp(os.P_WAIT, cmd, args)

            if status == 0:
                message = disk+' burn finished OK'

                for n in range(count-1):

                    print (say+message)

                    try_again = 1

                    while try_again:
                        dummy = raw_input('insert blank '+disk+' for disk %d and hit any key'%(n+2))
                        status = os.spawnvp(os.P_WAIT, cmd, args)

                        if status == 0:
                            try_again = 0
                            message = disk+' burn of disk %d finished OK'%(n+2)
                        else:
                            print (say+'something wrong? Return status: %d'%status)
                            try_again = raw_input('try disk %d again (yes/no) ? [no]'%(n+2))
                            try_again = (try_again.lower())[0] == 'y'

                            if not try_again:
                                message = 'disk %d discontinued'%(n+2)
            else:
                message = 'something wrong? Return status: %d'%status

            if status == 0:
                if not is_image:
                    os.remove( cd_img )

        print ('\n'+cd_img, cd_size, 'bytes (', tomb( cd_size ), 'MB)\n')

    print (say+message)

    if email != "":
        run_cmd( 'echo "'+message+'" | mail '+email+' -s"'+message+'"', 0 )

    return status


if __name__ == '__main__':

    import sys

    alldirs  = args(sys.argv)

    if len(alldirs) == 1:
        print ("Syntax: burndisk [-dvd] <directory1 <directory2 ..> >")
        sys.exit()

    # Check for keywords

    burn_args = dict    \
        ( [                \
          ( 'make_tar', is_there( '-tar'   , sys.argv ) ),    \
          ( 'make_dvd', is_there( '-dvd'   , sys.argv ) ),    \
          ( 'make_img', is_there( '-img'   , sys.argv ) ),    \
          ( 'nosudo'  , is_there( '-nosudo', sys.argv ) ),    \
          ( 'verbose' , is_there( '-verbose',sys.argv ) ),    \
          ( 'tempdir' , start   ( '-temp=' , sys.argv ) ),    \
          ( 'count'   , start   ( '-count=', sys.argv ) ),    \
          ( 'speed'   , start   ( '-speed=', sys.argv ) ),    \
          ( 'dev'     , start   ( '-dev='  , sys.argv ) ),    \
          ( 'mode'    , start   ( '-mode=' , sys.argv ) ),    \
          ( 'email'   , start   ( '-email=', sys.argv ) ),    \
          ( 'exe'     , start   ( '-exe='  , sys.argv ) ),    \
          ( 'nojoliet', is_there( '-nojoliet',sys.argv) ),    \
          ( 'links'   , is_there( '-links' , sys.argv ) )    ] )

    # List of directories to be put on CD.
    # Drop alldirs[0] (name of this script)

    alldirs = alldirs[1:len(alldirs)]
    burndisk( alldirs, burn_args )

    sys.exit()
