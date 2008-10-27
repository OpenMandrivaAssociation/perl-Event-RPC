%define pkgname Event-RPC
%define filelist %{pkgname}-%{version}-filelist
%define NVR %{pkgname}-%{version}-%{release}
%define maketest 1

Name:      perl-Event-RPC
Summary:   Event-RPC - Event based transparent Client/Server RPC framework
Version:   1.01
Release:   %mkrel 1
License:   Artistic
Group:     Development/Perl
URL:       http://www.exit1.org/Event-RPC
SOURCE:    http://search.cpan.org//CPAN/authors/id/J/JR/JRED/Event-RPC-%version.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-%(id -u -n)
Buildarch: noarch
BuildRequires: perl-devel
BuildRequires: perl-Event
BuildRequires: perl-IO-Socket-SSL
BuildConflicts: perl-Net_SSLeay < 1.30

%description
Event::RPC consists of a server and a client library. The server
exports a list of classes and methods, which are allowed to be called
over the network. More specific it acts as a proxy for objects created
on the server side (on demand of the connected clients) which handles
client side methods calls with transport of method arguments and
return values.

The object proxy handles refcounting and destruction of objects
created by clients properly. Objects as method parameters and return
values are handled as well (although with some limitations, see
below).

For the client the whole thing is totally transparent - once connected
to the server it doesn't know whether it calls methods on local or
remote objects.

Also the methods on the server newer know whether they are called
locally or from a connected client. Your application logic is not
affected by Event::RPC at all, at least if it has a rudimentary clean
OO design.

For details on implementing servers and clients please refer to the
man pages of Event::RPC::Server and Event::RPC::Client.

%prep
%setup -q -n %{pkgname}-%{version} 
chmod -R u+w %{_builddir}/%{pkgname}-%{version}

%build
grep -rsl '^#!.*perl' . |
grep -v '.bak$' |xargs --no-run-if-empty \
%__perl -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)'
CFLAGS="$RPM_OPT_FLAGS"
%{__perl} Makefile.PL `%{__perl} -MExtUtils::MakeMaker -e ' print qq|PREFIX=%{buildroot}%{_prefix}| if \$ExtUtils::MakeMaker::VERSION =~ /5\.9[1-6]|6\.0[0-5]/ '` INSTALLDIRS=vendor
%{__make} 
%check
%{__make} test

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%{makeinstall} `%{__perl} -MExtUtils::MakeMaker -e ' print \$ExtUtils::MakeMaker::VERSION <= 6.05 ? qq|PREFIX=%{buildroot}%{_prefix}| : qq|DESTDIR=%{buildroot}| '`

# remove special files
find %{buildroot} -name "perllocal.pod" \
    -o -name ".packlist"                \
    -o -name "*.bs"                     \
    |xargs -i rm -f {}

# no empty directories
find %{buildroot}%{_prefix}             \
    -type d -depth                      \
    -exec rmdir {} \; 2>/dev/null


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README Changes
%{perl_vendorlib}/Event/RPC*
%_mandir/man3/Event::RPC*

