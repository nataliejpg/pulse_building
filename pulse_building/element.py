import copy
from shutil import copyfile
from . import Waveform

# TODO: test 'check' behaviour
# TODO: write tests
# TODO: decide whether to limit setattr behaviour, code in waveform


class Element:
    def __init__(self):
        """
        Element class which represents the element of a sequence
        and is a dictionary of the waveforms running on channels of
        the AWG at one point in time.
        ie one element has many waveforms (one per channel)
           one sequence has many elements
        """

        self._waveforms = {}

    def __getitem__(self, key):
        return self._waveforms[key]

    def __setitem__(self, key, value):
        if not isinstance(key, int):
            raise TypeError('to add waveform to element an integer '
                            'channel value must be specified')
        elif not isinstance(value, Waveform):
            raise TypeError('waveform must be of type Waveform')
        self._waveforms[key] = value

    def __repr__(self):
        return repr(self._waveforms)

    def __len__(self):
        return len(self._waveforms)

    def __delitem__(self, key):
        del self._waveforms[key]

    def clear(self):
        """
        Function which empties dictionary
        """
        self._waveforms.clear()

    def add_waveform(self, waveform):
        """
        Function which adds a Waveform to the waveform dictionary
        """
        if not isinstance(waveform, Waveform):
            raise TypeError('cannot add waveform not of type Waveform')
        self[waveform.channel] = waveform

    def check(self):
        """
        Function which checks the element dictionary to have nonzero
        length and that all the waveforms in the dictionary are of
        equal length and then calls the waveform internal check on each.
        """
        if not self._waveforms:
            raise Exception('no waveforms in element')
        lengths = [w.length for w in self._waveforms.values()]
        if lengths.count(lengths[0]) != len(lengths):
            raise Exception(
                'the waveforms of this element are '
                'not of equal length: {}'.format(str(lengths)))
        for i, waveform in enumerate(self._waveforms.values()):
            try:
                waveform.check()
            except Exception as e:
                raise Exception(
                    'error in waveform {}: {}'.format(i, e))
        return True

    def unwrap_4dsp(self, folder):
        f = open(folder + 'waveform_0.txt', 'w')
        c_16B2CMAX = 32767
        l_wave = list(self.values())[0].length
        l_chans = len(list(self.keys())) * 3
        chans = list(self.keys())
        chans.sort()
        if l_chans > 6:
            raise ValueError('num of chans needed for waveforms'
                             ' plus markers not 6')

        # write the sizes to the file
        for ch in range(8):
            f.write(str(l_wave) + '\n')

        # compute the waveform samples and write them to the file
        for s in range(l_wave):
            for ch in chans:
                f.write(str(int(self._waveforms[ch].wave[s] * c_16B2CMAX)) + '\n')
                f.write(str(int(self._waveforms[ch].marker_1[s] * c_16B2CMAX)) + '\n')
                f.write(str(int(self._waveforms[ch].marker_2[s] * c_16B2CMAX)) + '\n')
            for i in range(8 - l_chans):
                f.write('0\n')

        # close the file
        f.close()

        for i in range(1, 6):
            copyfile(folder + 'waveform_0.txt', folder + 'waveform_{}.txt'.format(i))

    def copy(self):
        return copy.copy(self)

    def has_key(self, k):
        return k in self._waveforms

    def update(self, *args, **kwargs):
        return self._waveforms.update(*args, **kwargs)

    def keys(self):
        return self._waveforms.keys()

    def values(self):
        return self._waveforms.values()

    def items(self):
        return self._waveforms.items()

    def pop(self, *args):
        return self._waveforms.pop(*args)

    def __cmp__(self, dict):
        return cmp(self._waveforms, dict)

    def __contains__(self, item):
        return item in self._waveforms

    def __iter__(self):
        return iter(self._waveforms)
