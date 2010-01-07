Name:		rteval-xmlrpc
Version:	1.1
Release:	1%{?dist}
Summary:	XML-RPC server and parser for rteval

Group:		Applications/System
License:	GPLv2
URL:		http://git.kernel.org/?p=linux/kernel/git/clrkwllms/rteval.git
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql-devel libxml2-devel libxslt-devel
Requires:	postgresql httpd mod_python

%description
The XML-RPC server is using Apache and mod_python to receieve reports from
rteval clients submitting test results via an XML-RPC API.  The XML parser
daemon will parse the received reports and save them in a database for
further processing.


%prep
%setup -q


%build
%configure --with-xmlrpc-webroot=%{_localstatedir}/www/html/rteval --docdir=%{_defaultdocdir}/%{name}-%{version}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d
cp apache-rteval.conf $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/rteval-xmlrpc.conf


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README.xmlrpc parser/README.parser sql/rteval-%{version}.sql sql/delta-*_*.sql
%config(noreplace) %{_sysconfdir}/httpd/conf.d/rteval-xmlrpc.conf
%{_localstatedir}/www/html/rteval/
%{_bindir}/rteval_parserd
%{_datadir}/rteval/xmlparser.xsl


%changelog
* Tue Dec  8 2009 David Sommerseth <davids@redhat.com> - 1.1-1
- Updated to rteval-xmlrpc v1.1
  - Added new database table, rteval_info, containing some information about the
    rteval-xmlrpc installation
  - Made rteval_parserd aware of which SQL schema version it is working against
  - Added 'schemaver' attributes to <sqldata/> tags, defining which SQL schema
    version which is needed
  - Added mean_absolute_deviation and variance fields from rteval XML reports to
    the database

* Thu Dec  3 2009 David Sommerseth <davids@redhat.com> - 1.0-1
- Inital rteval-xmlrpc.spec file
