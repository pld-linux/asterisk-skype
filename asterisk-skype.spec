%define		dl_url	http://downloads.digium.com/pub/telephony/skypeforasterisk/asterisk-%{asterisk_ver}/
%define		asterisk_ver	1.6.1
Summary:	Digium's Skype For Asterisk
Name:		asterisk-skype
Version:	1.0.6
Release:	1
License:	Proprietary
Group:		Applications/System
Source0:	%{dl_url}/x86-32/skypeforasterisk-%{asterisk_ver}_%{version}-x86_32.tar.gz
# NoSource0-md5:	956264998c994f184fc7310aae63d2d4
NoSource:	0
Source1:	%{dl_url}/x86-64/skypeforasterisk-%{asterisk_ver}_%{version}-x86_64.tar.gz
# NoSource1-md5:	18050344e5ed4edcf03953a863d248e7
NoSource:	1
URL:		http://www.digium.com/skype/
BuildRequires:	asterisk-devel >= %{asterisk_ver}
BuildRequires:	sed >= 4.0
Requires:	asterisk >= %{asterisk_ver}
Requires:	group(asterisk)
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/asterisk
%define		moduledir	%{_libdir}/asterisk/modules

%description
Skype For Asterisk (SFA) is the first and only native channel driver
to connect Asterisk to the Skype network. The channel driver supports
an unlimited number of simultaneous users and an unlimited number of
simultaneous calls per user (subject to license key restriction).

Please visit the following web address to read more about this product
and to purchase license keys: <http://www.digium.com/skype/>.

%prep
%ifarch %{ix86}
%setup -qT -n skypeforasterisk-%{asterisk_ver}_%{version}-x86_64 -b0
%endif
%ifarch %{x8664}
%setup -qT -n skypeforasterisk-%{asterisk_ver}_%{version}-x86_64 -b1
%endif

%{__sed} -i -e '
s,%{_prefix}/lib/asterisk,%{_libdir}/asterisk,
	s,gcc,$(CC),g
	s,-pipe -O3,$(CFLAGS),g
' Makefile

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{moduledir}}
%{__make} install samples \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README chan_skype.conf.sample
%attr(640,root,asterisk) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/chan_skype.conf
%attr(755,root,root) %{moduledir}/chan_skype.so
%attr(755,root,root) %{moduledir}/res_skypeforasterisk.so
