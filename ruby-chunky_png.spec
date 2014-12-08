#
# Conditional build:
%bcond_without	tests		# build without tests
%bcond_without	doc			# don't build ri/rdoc

%define	pkgname chunky_png
Summary:	Pure ruby library for read/write, chunk-level access to PNG files
Name:		ruby-%{pkgname}
Version:	1.2.7
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://rubygems.org/gems/%{pkgname}-%{version}.gem
# Source0-md5:	3b872b1054bd3f586413d9169237432f
Patch0:		ruby-2.0.0.patch
URL:		http://wiki.github.com/wvanbergen/chunky_png
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	ruby-rspec
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This pure Ruby library can read and write PNG images without depending
on an external image library, like RMagick. It tries to be memory
efficient and reasonably fast.

It supports reading and writing all PNG variants that are defined in
the specification, with one limitation: only 8-bit color depth is
supported. It supports all transparency, interlacing and filtering
options the PNG specifications allows. It can also read and write
textual metadata from PNG files. Low-level read/write access to PNG
chunks is also possible. This library supports simple drawing on the
image canvas and simple operations like alpha composition and
cropping. Finally, it can import from and export to RMagick for
interoperability.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build
# write .gemspec
%__gem_helper spec

%if %{with tests}
# Don't use Bundler.
sed -i "/require 'bundler\/setup'/ s/^/#/" spec/spec_helper.rb

rspec spec
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rdoc LICENSE BENCHMARKS.rdoc benchmarks
%{ruby_vendorlibdir}/chunky_png.rb
%{ruby_vendorlibdir}/chunky_png
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
