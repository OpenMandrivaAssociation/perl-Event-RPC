%define pkgname Event-RPC
%define filelist %{pkgname}-%{upstream_version}-filelist
%define NVR %{pkgname}-%{upstream_version}-%{release}
%define maketest 1
%define upstream_version 1.05
Name:		perl-Event-RPC
Summary:	Event-RPC - Event based transparent Client/Server RPC framework
Version:	%perl_convert_version %{upstream_version}
Release:	3
License:	Artistic
Group:		Development/Perl
URL:		http://www.exit1.org/Event-RPC
Source:		http://search.cpan.org//CPAN/authors/id/J/JR/JRED/Event-RPC-%{upstream_version}.tar.gz

BuildRequires:	perl-devel
BuildRequires:	perl(Event)
BuildRequires:	perl(IO::Socket::SSL)
BuildConflicts:	perl-Net_SSLeay < 1.30
BuildArch: noarch

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
%setup -q -n %{pkgname}-%{upstream_version} 
chmod -R u+w %{_builddir}/%{pkgname}-%{upstream_version}

%build
grep -rsl '^#!.*perl' . |
grep -v '.bak$' |xargs --no-run-if-empty \
perl -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)'
CFLAGS="%{optflags}"
perl Makefile.PL `perl -MExtUtils::MakeMaker -e ' print qq|PREFIX=%{buildroot}%{_prefix}| if \$ExtUtils::MakeMaker::VERSION =~ /5\.9[1-6]|6\.0[0-5]/ '` INSTALLDIRS=vendor
make

%check
make test

%install
%makeinstall_std `perl -MExtUtils::MakeMaker -e ' print \$ExtUtils::MakeMaker::VERSION <= 6.05 ? qq|PREFIX=%{buildroot}%{_prefix}| : qq|DESTDIR=%{buildroot}| '`

# remove special files
find %{buildroot} -name "perllocal.pod" \
    -o -name ".packlist"                \
    -o -name "*.bs"                     \
    |xargs -i rm -f {}

# no empty directories
find %{buildroot}%{_prefix}             \
    -type d -depth                      \
    -exec rmdir {} \; 2>/dev/null

%files
%doc README Changes
%{perl_vendorlib}/Event/RPC*
%{_mandir}/man3/Event::RPC*


%changelog
* Tue Jul 26 2011 Götz Waschk <waschk@mandriva.org> 1.10.0-2mdv2012.0
+ Revision: 691694
- rebuild

* Tue Jul 28 2009 Götz Waschk <waschk@mandriva.org> 1.10.0-1mdv2011.0
+ Revision: 401501
- use perl version macro

* Mon Oct 27 2008 Götz Waschk <waschk@mandriva.org> 1.01-1mdv2009.1
+ Revision: 297529
- update to new version 1.01

* Sun Jun 22 2008 Götz Waschk <waschk@mandriva.org> 1.00-1mdv2009.0
+ Revision: 227956
- new version

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Mon Jul 31 2006 Götz Waschk <waschk@mandriva.org> 0.90-1mdv2007.0
- Rebuild

* Mon Apr 24 2006 Götz Waschk <waschk@mandriva.org> 0.90-1mdk
- New release 0.90

* Tue Mar 28 2006 Götz Waschk <waschk@mandriva.org> 0.89-1mdk
- New release 0.89

* Fri Jan 27 2006 Götz Waschk <waschk@mandriva.org> 0.88-2mdk
- reenable SSL

* Mon Dec 26 2005 Götz Waschk <waschk@mandriva.org> 0.88-1mdk
- New release 0.88

* Mon Dec 19 2005 Götz Waschk <waschk@mandriva.org> 0.87-1mdk
- New release 0.87

* Tue Aug 30 2005 Götz Waschk <waschk@mandriva.org> 0.85-1mdk
- New release 0.85

* Wed Aug 03 2005 Götz Waschk <waschk@mandriva.org> 0.84-1mdk
- initial package



