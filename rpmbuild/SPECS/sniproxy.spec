Name: sniproxy
Version: 0.5.0
Release: 1%{?dist}
Summary: Transparent TLS proxy

Group: System Environment/Daemons
License: BSD
URL: https://github.com/dlundquist/sniproxy
Source0: https://github.com/dlundquist/sniproxy/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: sniproxy.conf
Source2: sniproxy.service

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: curl
BuildRequires: systemd
BuildRequires: libev-devel
BuildRequires: pcre-devel
BuildRequires: perl
BuildRequires: udns-devel
# for lib-prefix.m4
BuildRequires: gettext-devel
# required for EL
BuildRequires: perl(Time::HiRes)

Requires(pre):    shadow-utils
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
SNIproxy proxies incoming HTTP and TLS connections based on the host name 
contained in the initial request. This enables HTTPS name based virtual 
hosting to separate back-end servers without the installing the private
key on the proxy machine.


%prep
%setup -q

%build
./autogen.sh
%configure CFLAGS="-I/usr/include/libev"
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/
install -p -m 644 %{SOURCE2} %{buildroot}%{_unitdir}

#%check
#make check

%pre
getent group sniproxy &>/dev/null || groupadd -r sniproxy
getent passwd sniproxy &>/dev/null || \
    /usr/sbin/useradd -r -g sniproxy -s /sbin/nologin -c sniproxy \
    -d / sniproxy

%post
%systemd_post sniproxy.service

%preun
%systemd_preun sniproxy.service

%postun
%systemd_postun sniproxy.service

%files

%config(noreplace) %{_sysconfdir}/sniproxy.conf

%{_sbindir}/sniproxy
%doc COPYING README.md AUTHORS ChangeLog
%{_unitdir}/sniproxy.service
%{_mandir}/man8/sniproxy.8*
%{_mandir}/man5/sniproxy.conf.5*

%changelog
* Wed Oct 18 2017 sniproxy - 0.5.0-1
- Initial version of the package
