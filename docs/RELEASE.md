# How to create a release

1. Update [issues](https://github.com/SynBioDex/pySBOL2/issues) and
   [pull requests](https://github.com/SynBioDex/pySBOL2/pulls) so they
   are appropriately targeted for this milestone and closed
1. Ensure all changes are described in the
   [CHANGES.md](https://github.com/SynBioDex/pySBOL2/blob/master/CHANGES.md)
   file
1. Tag the release using [semantic versioning](http://semver.org)

   ```shell
   cd <pySBOL2>
   git checkout master
   git tag -a v1.X -m "Release 1.X" master
   git push origin --tags
   ```

1. Update GitHub [milestones](https://github.com/SynBioDex/pySBOL2/milestones)
   * Close the current milestone
   * Create a new milestone for the next release
1. Create distribution wheel and source tarball

   ```shell
   cd <pySBOL2>
   python3 setup.py sdist bdist_wheel
   ls dist
   ```

1. Create a GitHub release, upload the wheel and source tarball
   * [Create a release](https://github.com/SynBioDex/pySBOL2/releases/new) (Releases; Draft a new release)
   * Use the current tag
   * Name it "Major.Minor[.Patch]"
   * Paste in the headings bullets from CHANGES.md for this release
   * Upload the source tar file and the wheel
1. Bump the version numbers on the develop branches
   * _Note: Use the standard contribution process by submitting these
     changes via a pull request on your fork, not a direct push to the
     SynBioDex repository_
   * Add a new version line to `CHANGES.md`
   * Bump version number in `setup.py`
   * Bump version number in the `sbol2/__init__.py