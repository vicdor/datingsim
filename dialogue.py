class Dialogue(object):
    """A Dialogue is a passage of text, divided into chunks that are
    to be displayed one-by-one."""
    def __init__(self, chunks):
        """@param chunks either a list of strings or a string. The string will be converted into
        a list consisting of that string.
        """
        if isinstance(chunks, list):
            for e in chunks:
                assert isinstance(e, str)
        elif isinstance(chunks, str):
            chunks = [chunks]
        self.chunks = chunks
        self.position = 0

    def show_all(self):
        """Calls show_next repeatedly until there is no more to show."""
        while self.has_more():
            self.show_next()

    def show_next(self):
        print(self.chunk[self.position])
        self.position += 1

    def peek(self):
        """Returns the next chunk to displayed (a string). Internally, the Dialogue object
        acts as if this chunk has not been accessed yet."""
        return self.chunk[self.position]

    def has_more(self):
        """Returns whether more chunks of text remain."""
        return self.position < len(self)

    def __len__(self):
        """The number of chunks of text that are displayed by this Dialogue."""
        return len(self.chunks)

class SelfPacedDialogue(Dialogue):
    """Waits for user to press return with each show_next."""
    def show_next(self):
        input(self.chunks[self.position])
        self.position += 1
